import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = util.env(cr)

    image_obj = env["base_multi_image.image"]
    attachment_obj = env["ir.attachment"]
    with open("/opt/odoo/attachments") as f:
        for line in f:
            try:
                image_id, attachment_id = line.strip().split("-")
                image = image_obj.browse(int(image_id))
                attachment = attachment_obj.browse(int(attachment_id))
                if image and attachment:
                    image.image_1920 = attachment.datas
                    _logger.info(
                        "Base multi image %s has been marked for migration",
                        image.id,
                    )
            except Exception as e:
                _logger.error(
                    "Error migrating base multi image %s: %s",
                    image_id,
                    e,
                )

    _logger.info("Migration of base multi images completed")
