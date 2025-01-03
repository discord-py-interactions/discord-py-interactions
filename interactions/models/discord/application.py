from typing import TYPE_CHECKING, List, Optional, Dict, Any

import attrs

from interactions.client.const import MISSING
from interactions.client.utils.attr_converters import optional
from interactions.client.utils.serializer import to_image_data
from interactions.models.discord.asset import Asset
from interactions.models.discord.emoji import CustomEmoji
from interactions.models.discord.enums import ApplicationFlags
from interactions.models.discord.file import UPLOADABLE_TYPE
from interactions.models.discord.snowflake import Snowflake_Type, to_snowflake
from interactions.models.discord.team import Team
from .base import DiscordObject

if TYPE_CHECKING:
    from interactions.client import Client
    from interactions.models import User

__all__ = ("Application",)


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class Application(DiscordObject):
    """Represents a discord application."""

    name: str = attrs.field(repr=True)
    """The name of the application"""
    icon: Optional[Asset] = attrs.field(repr=False, default=None)
    """The icon of the application"""
    description: Optional[str] = attrs.field(repr=False, default=None)
    """The description of the application"""
    rpc_origins: Optional[List[str]] = attrs.field(repr=False, default=None)
    """An array of rpc origin urls, if rpc is enabled"""
    bot_public: bool = attrs.field(repr=False, default=True)
    """When false only app owner can join the app's bot to guilds"""
    bot_require_code_grant: bool = attrs.field(repr=False, default=False)
    """When true the app's bot will only join upon completion of the full oauth2 code grant flow"""
    terms_of_service_url: Optional[str] = attrs.field(repr=False, default=None)
    """The url of the app's terms of service"""
    privacy_policy_url: Optional[str] = attrs.field(repr=False, default=None)
    """The url of the app's privacy policy"""
    owner_id: Optional[Snowflake_Type] = attrs.field(repr=False, default=None, converter=optional(to_snowflake))
    """The id of the owner of the application"""
    summary: str = attrs.field(
        repr=False,
    )
    """If this application is a game sold on Discord, this field will be the summary field for the store page of its primary sku"""
    verify_key: Optional[str] = attrs.field(repr=False, default=MISSING)
    """The hex encoded key for verification in interactions and the GameSDK's GetTicket"""
    team: Optional["Team"] = attrs.field(repr=False, default=None)
    """If the application belongs to a team, this will be a list of the members of that team"""
    guild_id: Optional["Snowflake_Type"] = attrs.field(repr=False, default=None)
    """If this application is a game sold on Discord, this field will be the guild to which it has been linked"""
    primary_sku_id: Optional["Snowflake_Type"] = attrs.field(repr=False, default=None)
    """If this application is a game sold on Discord, this field will be the id of the "Game SKU" that is created, if exists"""
    slug: Optional[str] = attrs.field(repr=False, default=None)
    """If this application is a game sold on Discord, this field will be the URL slug that links to the store page"""
    cover_image: Optional[Asset] = attrs.field(repr=False, default=None)
    """The application's default rich presence invite cover"""
    flags: Optional["ApplicationFlags"] = attrs.field(repr=False, default=None, converter=optional(ApplicationFlags))
    """The application's public flags"""
    tags: Optional[List[str]] = attrs.field(repr=False, default=None)
    """The application's tags describing its functionality and content"""
    # todo: implement an ApplicationInstallParams object. See https://discord.com/developers/docs/resources/application#install-params-object
    install_params: Optional[dict] = attrs.field(repr=False, default=None)
    """The application's settings for in-app invitation to guilds"""
    # todo: implement IntegrationTypeConfigurationObject too, see https://discord.com/developers/docs/resources/application#application-object-application-integration-type-configuration-object
    integration_types_config: Optional[dict] = attrs.field(repr=False, default=None)
    """Default scopes and permissions for each supported installation context. Value for each key is an integration type configuration object"""
    custom_install_url: Optional[str] = attrs.field(repr=False, default=None)
    """The application's custom authorization link for invitation to a guild"""

    @classmethod
    def _process_dict(cls, data: Dict[str, Any], client: "Client") -> Dict[str, Any]:
        if data.get("team"):
            data["team"] = Team.from_dict(data["team"], client)
            data["owner_id"] = data["team"].owner_user_id
        elif "owner" in data:
            owner = client.cache.place_user_data(data.pop("owner"))
            data["owner_id"] = owner.id

        if data.get("icon"):
            data["icon"] = Asset.from_path_hash(client, f"app-icons/{data['id']}/{{}}", data["icon"])
        if data.get("cover_image"):
            data["cover_image"] = Asset.from_path_hash(client, f"app-icons/{data['id']}/{{}}", data["cover_image"])

        return data

    @property
    def owner(self) -> "User":
        """The user object for the owner of this application"""
        return self._client.cache.get_user(self.owner_id)

    async def fetch_all_emoji(self) -> List[CustomEmoji]:
        """Fetch all emojis for this application"""
        response = await self.client.http.get_application_emojis(self.id)
        return [self.client.cache.place_emoji_data(None, emoji) for emoji in response]

    async def fetch_emoji(self, emoji_id: Snowflake_Type) -> CustomEmoji:
        """Fetch an emoji for this application"""
        response = await self.client.http.get_application_emoji(self.id, emoji_id)
        return self.client.cache.place_emoji_data(None, response)

    async def create_emoji(self, name: str, imagefile: UPLOADABLE_TYPE) -> CustomEmoji:
        """Create an emoji for this application"""
        data_payload = {
            "name": name,
            "image": to_image_data(imagefile),
            "roles": MISSING,
        }

        return self.client.cache.place_emoji_data(
            None, await self.client.http.create_application_emoji(data_payload, self.id)
        )

    async def edit_emoji(self, emoji_id: Snowflake_Type, name: str) -> CustomEmoji:
        """Edit an emoji for this application"""
        return self.client.cache.place_emoji_data(
            None, await self.client.http.edit_application_emoji(self.id, emoji_id, name)
        )

    async def delete_emoji(self, emoji_id: Snowflake_Type) -> None:
        """Delete an emoji for this application"""
        await self.client.http.delete_application_emoji(self.id, emoji_id)
