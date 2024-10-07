from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton
from bot.models.StreamerManager import save_data, StreamerManager
from bot.states.SetPercentState import SetPercentState
from bot.keyboards.keyboard import main
from bot.utils.manager import get_table_value

router = Router()
manager = StreamerManager()


@router.message(F.text == "Add streamer")
async def add_streamer(message: Message, state: FSMContext):
    await message.answer("Введите имя канала для добавления:")
    await state.set_state(SetPercentState.channel_name_add)


@router.message(SetPercentState.channel_name_add)
async def process_add_streamer(message: Message, state: FSMContext):
    channel_name = message.text
    if channel_name in ["Add streamer", "Delete streamer", "My Streamers", "Start monitoring", "Stop monitoring",
                        "Set min %", "Set max %", "Узнать текущее состояние"]:
        await state.clear()
        await message.answer("Пожалуйста, введите корректное имя стримера, а не команду.")
        return
    manager.add_streamer(channel_name)
    save_data(manager.get_streamers())
    percent = await get_table_value(channel_name)
    manager.update_percent(channel_name, percent)
    await message.answer(f"Стример {channel_name} успешно добавлен.", reply_markup=main)
    await state.clear()


@router.message(F.text == "Delete streamer")
async def remove_streamer(message: Message, state: FSMContext):
    streamers = manager.get_streamers()

    if not streamers:
        await message.answer("Нет стримеров для удаления.")
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=streamer, callback_data=f"delete_{streamer}")]
            for streamer in streamers
        ])

        await message.answer("Выберите стримера для удаления:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("delete_"))
async def process_remove_streamer(callback: CallbackQuery, state: FSMContext):
    channel_name = callback.data.split("_")[1]

    if channel_name in manager.get_streamers():
        manager.remove_streamer(channel_name)
        await callback.message.edit_text(f"Стример {channel_name} удален.", reply_markup=None)
    else:
        await callback.message.edit_text(f"Стример {channel_name} не найден.", reply_markup=None)
    await state.clear()


@router.message(F.text == "My Streamers")
async def list_streamers(message: Message, state: FSMContext):
    streamers = manager.get_streamers()
    if streamers:
        response = "Отслеживаемые стримеры:\n"
        for channel, info in streamers.items():
            percent = await get_table_value(channel)
            manager.update_percent(channel, percent)
            response += f"{channel}: {percent}%\n"
        await message.answer(response)
    else:
        await message.answer("Нет отслеживаемых стримеров.")


# @router.message(F.text == "Active streamers")
# async def show_active_streamers(message: Message):
#     streamers = get_active_streamers()
#     if not streamers:
#         await message.answer("Не удалось получить список активных стримеров.")
#         return
#     messages = "\n".join(streamers)
#     await message.answer(f"Активные стримеры:\n{messages}")
