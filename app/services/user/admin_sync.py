from loguru import logger
from sqlalchemy import update

from app.bot.instance import bot, dp
from app.storage.instance import async_session
from app.storage.models.user import Role, User
from app.utils.state.data import update_data


async def sync_admin_roles(admins: list[int]):
    admin_ids = set(admins)

    logger.debug(
        "Synchronizing admin access",
        admin_count=len(admin_ids),
        admin_ids=sorted(admin_ids),
    )

    async with async_session() as session:
        promoted = await session.execute(
            update(User)
            .where(User.telegram_id.in_(admin_ids))
            .values(role=Role.ADMIN)
            .returning(User.telegram_id)
        )
        promoted_admins = promoted.scalars().all()

        demoted = await session.execute(
            update(User)
            .where(User.role == Role.ADMIN)
            .where(~User.telegram_id.in_(admin_ids))
            .values(role=Role.USER)
            .returning(User.telegram_id)
        )
        demoted_admins = demoted.scalars().all()

        await session.commit()

    for id in promoted_admins:
        await update_data(bot, dp, id, {"sender_role": Role.ADMIN}, "long")

    logger.info(
        "Admin access synchronized",
        promoted=promoted_admins,
        demoted=demoted_admins,
    )
