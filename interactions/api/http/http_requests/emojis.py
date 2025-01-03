from typing import TYPE_CHECKING, cast

import discord_typings

from interactions.models.internal.protocols import CanRequest
from ..route import Route

__all__ = ("EmojiRequests",)


if TYPE_CHECKING:
    from interactions.models.discord.snowflake import Snowflake_Type


class EmojiRequests(CanRequest):
    async def get_all_guild_emoji(self, guild_id: "Snowflake_Type") -> list[discord_typings.EmojiData]:
        """
        Get all the emoji from a guild.

        Args:
            guild_id: The ID of the guild to query.

        Returns:
            List of emoji objects

        """
        result = await self.request(Route("GET", "/guilds/{guild_id}/emojis", guild_id=guild_id))
        return cast(list[discord_typings.EmojiData], result)

    async def get_guild_emoji(
        self, guild_id: "Snowflake_Type", emoji_id: "Snowflake_Type"
    ) -> discord_typings.EmojiData:
        """
        Get a specific guild emoji object.

        Args:
            guild_id: The ID of the guild to query
            emoji_id: The ID of the emoji to get

        Returns:
            PartialEmoji object

        """
        result = await self.request(
            Route("GET", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id)
        )
        return cast(discord_typings.EmojiData, result)

    async def create_guild_emoji(
        self, payload: dict, guild_id: "Snowflake_Type", reason: str | None = None
    ) -> discord_typings.EmojiData:
        """
        Create a guild emoji.

        Args:
            payload: The emoji's data
            guild_id: The ID of the guild
            reason: The reason for this creation

        Returns:
            The created emoji object

        """
        result = await self.request(
            Route("POST", "/guilds/{guild_id}/emojis", guild_id=guild_id), payload=payload, reason=reason
        )

        return cast(discord_typings.EmojiData, result)

    async def modify_guild_emoji(
        self,
        payload: dict,
        guild_id: "Snowflake_Type",
        emoji_id: "Snowflake_Type",
        reason: str | None = None,
    ) -> discord_typings.EmojiData:
        """
        Modify an existing guild emoji.

        Args:
            payload: The emoji's data
            guild_id: The ID of the guild
            emoji_id: The ID of the emoji to update
            reason: The reason for this creation

        Returns:
            The updated emoji object

        """
        result = await self.request(
            Route("PATCH", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id),
            payload=payload,
            reason=reason,
        )
        return cast(discord_typings.EmojiData, result)

    async def delete_guild_emoji(
        self, guild_id: "Snowflake_Type", emoji_id: "Snowflake_Type", reason: str | None = None
    ) -> None:
        """
        Delete a guild emoji.

        Args:
            guild_id: The ID of the guild
            emoji_id: The ID of the emoji to update
            reason: The reason for this deletion

        """
        await self.request(
            Route("DELETE", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id),
            reason=reason,
        )

    async def get_application_emojis(self, application_id: "Snowflake_Type") -> list[discord_typings.EmojiData]:
        """
        Fetch all emojis for this application

        Args:
            application_id: The id of the application

        Returns:
            List of emojis

        """
        result = await self.request(Route("GET", f"/applications/{application_id}/emojis"))
        result = cast(dict, result)
        return cast(list[discord_typings.EmojiData], result["items"])

    async def get_application_emoji(
        self, application_id: "Snowflake_Type", emoji_id: "Snowflake_Type"
    ) -> discord_typings.EmojiData:
        """
        Fetch an emoji for this application

        Args:
            application_id: The id of the application
            emoji_id: The id of the emoji

        Returns:
            Emoji object

        """
        result = await self.request(Route("GET", f"/applications/{application_id}/emojis/{emoji_id}"))
        return cast(discord_typings.EmojiData, result)

    async def create_application_emoji(
        self, payload: dict, application_id: "Snowflake_Type", reason: str | None = None
    ) -> discord_typings.EmojiData:
        """
        Create an emoji for this application

        Args:
            application_id: The id of the application
            name: The name of the emoji
            imagefile: The image file to use for the emoji

        Returns:
            Emoji object

        """
        result = await self.request(
            Route("POST", f"/applications/{application_id}/emojis"), payload=payload, reason=reason
        )
        return cast(discord_typings.EmojiData, result)

    async def edit_application_emoji(
        self, application_id: "Snowflake_Type", emoji_id: "Snowflake_Type", name: str
    ) -> discord_typings.EmojiData:
        """
        Edit an emoji for this application

        Args:
            application_id: The id of the application
            emoji_id: The id of the emoji
            name: The new name for the emoji

        Returns:
            Emoji object

        """
        result = await self.request(
            Route("PATCH", f"/applications/{application_id}/emojis/{emoji_id}"), payload={"name": name}
        )
        return cast(discord_typings.EmojiData, result)

    async def delete_application_emoji(
        self, application_id: discord_typings.Snowflake, emoji_id: discord_typings.Snowflake
    ) -> None:
        """
        Delete an emoji for this application

        Args:
            application_id: The id of the application
            emoji_id: The id of the emoji

        """
        await self.request(Route("DELETE", f"/applications/{application_id}/emojis/{emoji_id}"))
