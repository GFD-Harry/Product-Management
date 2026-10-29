from odoo import api, fields, models
from odoo.exceptions import ValidationError

LOW_STOCK_THRESHOLD = 5

import logging 
_logger = logging.getLogger(__name__)


class ProductManagementProduct(models.Model):
    _name = "product.management.product"
    _description = "Product Management Product"
    _order = "sequence, name"
    _name_unique_default_code = models.Constraint(
        "unique(default_code)",
        "A product with this internal reference already exists.",
    )

    default_code = fields.Char(string="Internal Reference")
    name = fields.Char(required=True)
    category_id = fields.Many2one(
        "product.management.category",
        string="Category",
        required=True,
        ondelete="restrict",
    )
    brand_id = fields.Many2one(
        "product.management.brand",
        string="Brand",
        ondelete="restrict",
    )
    purpose = fields.Text(string="Purpose")
    list_price = fields.Float(default=0.0)
    qty_available = fields.Integer(default=0)
    stock_status = fields.Selection(
        [
            ("in_stock", "In Stock"),
            ("low_stock", "Low Stock"),
            ("out_of_stock", "Out of Stock"),
        ],
        compute="_compute_stock_status",
        readonly=True,
        store=True,
    )
    product_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("available", "Available"),
            ("discontinued", "Discontinued"),
        ],
        default="draft",
        required=True,
    )
    image_1920 = fields.Image()
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    field_value_ids = fields.One2many(
        "product.management.product.field.value",
        "product_id",
        string="Specifications",
    )

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        products._sync_field_values_with_category()
        return products

    def write(self, vals):
        result = super().write(vals)
        if "category_id" in vals:
            self._sync_field_values_with_category()
        return result

    @api.onchange("category_id")
    def _onchange_category_id(self):
        self._sync_field_values_with_category()

    def _has_required_dynamic_value(self, value):
        if value.field_type == "char":
            return bool(value.value_char)
        if value.field_type == "text":
            return bool(value.value_text)
        if value.field_type == "integer":
            return value.value_integer is not False
        if value.field_type == "float":
            return value.value_float is not False
        if value.field_type == "boolean":
            return True
        if value.field_type == "date":
            return bool(value.value_date)
        if value.field_type == "datetime":
            return bool(value.value_datetime)
        if value.field_type == "selection":
            return bool(value.option_id)
        return False         

    @api.constrains("product_status", "category_id", "field_value_ids")
    def _check_required_field_values(self):
        for product in self:
            if product.product_status != "available":
                continue

            required_fields = product._get_active_category_fields().filtered("required")
            values_by_field = {
                value.field_id.id: value
                for value in product.field_value_ids
            }

            missing_field_names = []

            for field in required_fields:
                value = values_by_field.get(field.id)
                if not value or not product._has_required_dynamic_value(value):
                    missing_field_names.append(field.name)

            if missing_field_names:
                raise ValidationError(
                    "Cannot set product to Available because required specifications "
                    f"are missing: {', '.join(missing_field_names)}."
                )
                

    def _get_active_category_fields(self):
        self.ensure_one()
        if not self.category_id:
            return self.env["product.management.category.field"]
        return self.category_id.field_ids.filtered(lambda f: f.active)

    def _sync_field_values_with_category(self):
        for product in self:
            _logger.info(
                "[SYNC BEFORE] Category=%s, Values=%s",
                product.category_id.id,
                [
                    (v.id, v.field_id.id, v.required, v.product_id.id)
                    for v in product.field_value_ids
                ]
            )
            if not product.category_id:
                product.field_value_ids = [(5, 0, 0)]
                continue

            category_fields = product._get_active_category_fields()
            existing_values_by_field = {
                value.field_id.id: value
                for value in product.field_value_ids
            }

            commands = []

            for field in category_fields:
                if field.id in existing_values_by_field:
                    continue

                commands.append((0, 0, {"field_id": field.id}))

            obsolete_values = product.field_value_ids.filtered(
                lambda value: value.field_id not in category_fields
            )

            for value in obsolete_values:
                commands.append((2, value.id))

            if commands:
                product.field_value_ids = commands

            _logger.info(
                "[SYNC AFTER] Category=%s, Values=%s",
                product.category_id.id,
                [
                    (v.id, v.field_id.id, v.required, v.product_id.id)
                    for v in product.field_value_ids
                ]
            )

    @api.constrains("active", "product_status")
    def _check_active_product_status_consistency(self):
        for product in self:
            if not product.active and product.product_status == "available":
                raise ValidationError(
                    "An available product cannot be archived. "
                    "Set the product status to Discontinued before archiving."
                )

    @api.constrains("list_price")
    def _check_list_price_not_negative(self):
        for product in self:
            if product.list_price < 0:
                raise ValidationError("List price cannot be negative.")

    @api.constrains("qty_available")
    def _check_qty_available_not_negative(self):
        for product in self:
            if product.qty_available < 0:
                raise ValidationError("The quantity available cannot be negative.")

    @api.depends("qty_available")
    def _compute_stock_status(self):
        for product in self:
            if product.qty_available <= 0:
                product.stock_status = "out_of_stock"
            elif product.qty_available <= LOW_STOCK_THRESHOLD:
                product.stock_status = "low_stock"
            else:
                product.stock_status = "in_stock"

    # Comparison Logic
    def action_open_compare_wizard(self):
        products = self

        if len(products) < 2:
            raise ValidationError("Select at least two products to compare.")

        if len(products) > 4:
            raise ValidationError("You can compare a maximum of four products.")

        categories = products.mapped("category_id")
        if len(categories) != 1:
            raise ValidationError("All selected products must belong to the same category.")

        wizard = self.env["product.management.compare.wizard"].create({
            "product_ids": [(6, 0, products.ids)],
            "category_id": categories.id,
            "dynamic_field_ids": [(6, 0, categories.field_ids.filtered("active").ids)]
        })

        wizard._set_product_previews() # add preview images
        wizard._rebuild_result_lines()

        return {
            "type": "ir.actions.act_window",
            "name": "Compare Product",
            "res_model": "product.management.compare.wizard",
            "res_id": wizard.id,
            "view_mode": "form",
            "target": "new"
        }
