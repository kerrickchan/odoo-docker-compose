from odoo import api, fields, models


class HelloWorld(models.Model):
    _name = 'hello.world'
    _description = 'Hello World'

    name = fields.Char(string='Name', required=True)
    message = fields.Text(string='Message', default='Hello, World!')
    is_published = fields.Boolean(string='Published', default=False)

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"Hello, {record.name}!"
