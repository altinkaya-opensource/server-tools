import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute(
        """
        SELECT id, attachment_id
        FROM base_multi_image_image
        WHERE attachment_id IS NOT NULL
        """
    )

    base_multi_images = cr.fetchall() or []

    with open("/opt/odoo/attachments", "w") as f:
        for image in base_multi_images:
            f.write(f"{image[0]}-{image[1]}\n")
            _logger.info(
                "Base multi image %s has been marked for migration",
                image[0],
            )