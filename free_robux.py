"""
    🎯 RobuxPrank - Интерактивный пранк (Rick Roll)
    
    Отправляет красивое сообщение о "бесплатных робуксах".
    Кнопка ведет на Рик Ролл.
"""

version = (1, 0, 0)

# meta developer: @Gabsize
# scope: hikka_only
# scope: hikka_min 1.3.0

from .. import loader, utils
from herokutl.types import Message
import logging

logger = logging.getLogger(__name__)

@loader.tds
class RobuxPrankMod(loader.Module):
    """Пранк-модуль: Бесплатные Робуксы -> Rick Roll"""
    
    strings = {
        "name": "RobuxPrank",
        "scam_text": (
            "<b>💰 ROBLOX OFFICIAL EVENT</b>\n\n"
            "Congratulations! You have been selected to receive "
            "<b>100,000 ROBUX</b> for free!\n\n"
            "<i>Click the button below to claim your reward instantly.</i>"
        ),
        "button_text": "🎁 CLAIM 100k ROBUX 🎁",
        "no_inline": "❌ <b>Error:</b> Inline mode is not set up in your UserBot.",
    }
    
    strings_ru = {
        "scam_text": (
            "<b>💰 ОФИЦИАЛЬНЫЙ ИВЕНТ ROBLOX</b>\n\n"
            "Поздравляем! Вы были выбраны для получения "
            "<b>100,000 ROBUX</b> бесплатно!\n\n"
            "<i>Нажми на кнопку ниже, чтобы забрать награду прямо сейчас.</i>"
        ),
        "button_text": "🎁 ЗАБРАТЬ 100k ROBUX 🎁",
        "no_inline": "❌ <b>Ошибка:</b> Инлайн режим не настроен в вашем Юзерботе.",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "rickroll_url",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "Ссылка, куда ведет кнопка (Rick Roll)",
                validator=loader.validators.Link()
            ),
            loader.ConfigValue(
                "image_url",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Robux_2019_Logo_gold.svg/1200px-Robux_2019_Logo_gold.svg.png",
                "Ссылка на картинку для превью",
                validator=loader.validators.Link()
            )
        )

    async def client_ready(self, client, db):
        self._client = client
        
    @loader.command(
        ru_doc="Отправить фейк с робуксами (требуется Inline)",
        en_doc="Send fake robux message (requires Inline)"
    )
    async def scamcmd(self, message: Message):
        """Отправляет сообщение с кнопкой-ловушкой"""
        # Удаляем сообщение с командой, чтобы было беспалевно
        await message.delete()

        # Проверяем инициализацию инлайна
        if not hasattr(self, "inline"):
            await utils.answer(message, self.strings["no_inline"])
            return

        try:
            # Формируем инлайн-кнопки
            # URL кнопки берется из конфига
            buttons = [
                [
                    {
                        "text": self.strings["button_text"],
                        "url": self.config["rickroll_url"]
                    }
                ]
            ]

            # Отправляем форму через инлайн-бота
            await self.inline.form(
                text=self.strings["scam_text"],
                message=message,
                reply_markup=buttons,
                # Картинка для убедительности
                photo=self.config["image_url"] 
            )
            
        except Exception as e:
            logger.exception("Error sending scam form")
            # Если не удалось отправить инлайн, сообщаем пользователю (но не в чат, чтобы не спалиться)
            await utils.answer(message, f"❌ Error: {e}")