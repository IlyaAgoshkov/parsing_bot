import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.keyboards.keyboard import main
from bot.models.StreamerManager import StreamerManager
from bot.states.SetPercentState import SetPercentState
from bot.states.MonitoringStates import MonitoringStates
from bot.utils.manager import monitor_streamers

monitoring_router = Router()
manager = StreamerManager()


@monitoring_router.message(F.text == "Start monitoring")
async def start_monitoring(message: Message, state: FSMContext):
    manager.load_data()
    streamers = manager.get_streamers()
    if streamers:
        manager.set_monitoring_active(True)
        manager.load_data()
        await state.set_state(MonitoringStates.monitoring)
        await message.answer("Мониторинг запущен.")
        asyncio.create_task(monitor_streamers(message.from_user.id, message.bot, state))
    else:
        await message.answer("Нет стримеров для мониторинга.")


@monitoring_router.message(F.text == "Stop monitoring")
async def stop_monitoring(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Мониторинг остановлен.")


@monitoring_router.message(F.text == "Set min %")
async def set_min_percent(message: Message, state: FSMContext):
    await message.answer(f"Сейчас минимальный процент: {manager.min_percent}.\n"
                         f"Введите новый минимальный процент:")
    await state.set_state(SetPercentState.min_percent)


@monitoring_router.message(SetPercentState.min_percent)
async def process_min_percent(message: Message, state: FSMContext):
    if message.text in ["Add streamer", "Delete streamer", "My Streamers", "Start monitoring", "Stop monitoring",
                        "Set min %", "Set max %", "Узнать текущее состояние"]:
        await state.clear()
        await message.answer("Пожалуйста, введите корректное число, а не команду.")
        return

    try:
        min_percent = int(message.text)
        manager.set_min_percent(min_percent)
        await message.answer(f"Минимальный процент успешно установлен на {min_percent}%.", reply_markup=main)
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")


@monitoring_router.message(F.text == "Set max %")
async def set_max_percent(message: Message, state: FSMContext):
    await message.answer(f"Сейчас максимальный процент: {manager.max_percent}.\n"
                         f"Введите новый максимальный процент:")
    await state.set_state(SetPercentState.max_percent)


@monitoring_router.message(SetPercentState.max_percent)
async def process_max_percent(message: Message, state: FSMContext):
    if message.text in ["Add streamer", "Delete streamer", "My Streamers", "Start monitoring", "Stop monitoring",
                        "Set min %", "Set max %", "Узнать текущее состояние"]:
        await state.clear()
        await message.answer("Пожалуйста, введите корректное число, а не команду.")
        return

    try:
        max_percent = int(message.text)
        manager.set_max_percent(max_percent)
        await message.answer(f"Максимальный процент успешно установлен на {max_percent}%.", reply_markup=main)
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

