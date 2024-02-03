import os
import shutil
import PVRTexLibPy as pvrpy

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.request import get_admin, get_user, update_counters_convert, get_counter_convert
from app.admins import maintenance
import app.keyboards as kb


router = Router()


class Convert(StatesGroup):
    type = State()
    files = State()
    

@router.callback_query(F.data == 'convert_type_btxtopng')
async def convert_type_btxtopng(callback: CallbackQuery, state: FSMContext):
    if maintenance == True:
        await callback.message.answer('Внимание! Проходят технические обновления. Приносим извинения за временные неудобства.')
        return
    
    count_convert = await get_counter_convert(callback.message.from_user.id)
    
    """ if count_convert.today >= count_convert.limit:
        await callback.message.answer('Конвертация запрещена. Превышен лимит конвертаций в день.')
        return """
    
    await state.update_data(type='btxtopng')
    await state.set_state(Convert.files)
    await callback.message.answer('Отправьте файлы для конвертации:', reply_markup=kb.cancel_convert)


@router.callback_query(F.data == 'convert_type_pngtobtx')
async def convert_type_pngtobtx(callback: CallbackQuery, state: FSMContext):
    if maintenance == True:
        await callback.answer('Внимание! Проходят технические обновления. Приносим извинения за временные неудобства.')
        return
    
    count_convert = await get_counter_convert(callback.message.from_user.id)
    
    """ if count_convert.today >= count_convert.limit:
        await callback.answer('Конвертация запрещена. Превышен лимит конвертаций в день.')
        return """
    
    await state.update_data(type='pngtobtx')
    await state.set_state(Convert.files)
    await callback.message.answer('Отправьте файлы для конвертации:', reply_markup=kb.cancel_convert)


@router.message(F.text == 'Отмена', Convert.files)
async def cancel_convert(message: Message, state: FSMContext):
    await state.clear()

    if await get_admin(user_id=message.from_user.id):
        await message.answer('Операция отменена.', reply_markup=kb.main_admin)
    else:
        await message.answer('Операция отменена.', reply_markup=kb.main)


@router.message(Convert.files)
async def convert_files(message: Message, state: FSMContext):
    if maintenance == True:
        await message.answer('Внимание! Проходят технические обновления. Приносим извинения за временные неудобства.')
        return
    
    """ count_convert = await get_counter_convert(message.from_user.id)
    if count_convert.today >= count_convert.limit:
        await message.answer('Конвертация запрещена. Превышен лимит конвертаций в день.')
        return """
    
    fileformat = message.document.file_name[-4:]
    convert_state = await state.get_data()
    convert_type = convert_state['type']
    

    if convert_type == 'pngtobtx':
        if fileformat == '.png':
            try:
                file_id = message.document.file_id
                file_info = await message.bot.get_file(file_id)
                file_path = file_info.file_path
                file_name = message.document.file_name

                folder_path = "files_for_convert/" + str(message.from_user.id) + '/'
                if not os.path.exists(folder_path + 'input_files/'):
                    os.makedirs(folder_path + 'input_files/')
                    
                await message.bot.download_file(file_path, folder_path + 'input_files/' + file_name)
                await convert_pngtobtx(message, folder_path, file_name)

                output_folder_path = folder_path + 'output_files/'
                converted_file_name = os.path.splitext(output_folder_path + file_name)
                document_path = converted_file_name[0] + '.btx'
                
                cat = FSInputFile(document_path)
                if await get_admin(user_id=message.from_user.id):
                    await message.answer_document(cat, reply_markup=kb.main_admin)
                else:
                    await message.answer_document(cat, reply_markup=kb.main)
                

                os.remove(converted_file_name[0] + '.btx')
                os.remove(folder_path + 'input_files/' + file_name)

            except Exception as e:
                print('ERROR: ' + str(e))
                if await get_admin(user_id=message.from_user.id):
                    await message.answer('[Error #100] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>', reply_markup=kb.main_admin)
                else:
                    await message.answer('[Error #100] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>', reply_markup=kb.main)
        else:
            if await get_admin(user_id=message.from_user.id):
                await message.answer('[Warning #101] Неверный формат файла!', reply_markup=kb.main_admin)
            else:
                await message.answer('[Warning #101] Неверный формат файла!', reply_markup=kb.main)

    elif convert_type == 'btxtopng':
        if fileformat == '.btx':
            try:
                file_id = message.document.file_id
                file_info = await message.bot.get_file(file_id)
                file_path = file_info.file_path
                file_name = message.document.file_name

                folder_path = "files_for_convert/" + str(message.from_user.id) + '/'
                if not os.path.exists(folder_path + 'input_files/'):
                    os.makedirs(folder_path + 'input_files/')
                    
                await message.bot.download_file(file_path, folder_path + 'input_files/' + file_name)
                await convert_btxtopng(message, folder_path, file_name)

                output_folder_path = folder_path + 'output_files/'
                converted_file_name = os.path.splitext(output_folder_path + file_name)
                document_path = converted_file_name[0] + '.png'
                
                cat = FSInputFile(document_path)
                if await get_admin(user_id=message.from_user.id):
                    await message.answer_document(cat, reply_markup=kb.main_admin)
                else:
                    await message.answer_document(cat, reply_markup=kb.main)

                os.remove(converted_file_name[0] + '.png')
                os.remove(folder_path + 'input_files/' + file_name)
            except Exception as e:
                print('ERROR: ' + str(e))
                if await get_admin(user_id=message.from_user.id):
                    await message.answer('[Error #102] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>', reply_markup=kb.main_admin)
                else:
                    await message.answer('[Error #102] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>', reply_markup=kb.main)
        else:
            if await get_admin(user_id=message.from_user.id):
                await message.answer('[Warning #103] Неверный формат файла!', reply_markup=kb.main_admin)
            else:
                await message.answer('[Warning #103] Неверный формат файла!', reply_markup=kb.main)
                
    await update_counters_convert(user_id=message.from_user.id)

    await state.clear()


async def convert_pngtobtx(message: Message, path, filename):

    print(path + 'input_files/' + filename)

    filename1 = os.path.splitext(path + 'input_files/' + filename)

    await convertprocess_pngtobtx(path + 'input_files/' + filename, message)

    output_folder = path + 'output_files/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    shutil.move(filename1[0] + '.btx', output_folder)
    

async def convert_btxtopng(message: Message, path, filename):
    print(path + 'input_files/' + filename)

    ktx_file = open(path + 'input_files/' + filename, 'r+b')
    ktx_file.seek(4)
    remaining_content = ktx_file.read()
    ktx_file.seek(0)
    ktx_file.write(remaining_content)
    ktx_file.close()

    filename1 = os.path.splitext(path + 'input_files/' + filename)
    if filename1[1] == '.btx':
        os.rename(path + 'input_files/' + filename, filename1[0] + '.ktx')

    await convertprocess_btxtopng(filename1[0] + '.ktx', message)

    output_folder = path + 'output_files/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    shutil.move(filename1[0] + '.png', output_folder)

    filename2 = os.path.splitext(filename1[0] + '.ktx')
    if filename2[1] == '.ktx':
        os.rename(filename1[0] + '.ktx', filename1[0] + '.btx')


# ==================================== Лучше не лезь ====================================


async def convertprocess_pngtobtx(texturename, message: Message):
    texture = pvrpy.PVRTexture(texturename)

    if not texture.PreMultiplyAlpha():
        await message.answer('[Error #301] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)

    if not texture.Bleed():
        await message.answer('[Error #302] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)

    if not texture.GenerateMIPMaps(pvrpy.ResizeMode.Linear):
        await message.answer('[Error #303] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)

    if not texture.Transcode(pvrpy.PixelFormat.ASTC_4x4, pvrpy.VariableType.UnsignedByteNorm, pvrpy.ColourSpace.sRGB,
                             pvrpy.CompressorQuality.ASTCExhaustive):
        await message.answer('[Error #304] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)

    # sRGB создает потом надо на Linear, а то темно
    if texture.SetTextureColourSpace(pvrpy.ColourSpace.Linear) == False:
        await message.answer('[Error #305] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)

    texturename1 = os.path.splitext(texturename)

    if not texture.SaveToFile(texturename1[0] + ".ktx"):
        await message.answer('[Error #306] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)
        os.remove(texturename1[0] + ".ktx")

    ktx_file = open(texturename1[0] + '.ktx', 'r+b')
    original_bytes = ktx_file.read()
    ktx_file.seek(0)
    ktx_file.write(b'\x02\x00\x00\x00')
    ktx_file.write(original_bytes)
    ktx_file.close()

    filename2 = os.path.splitext(texturename1[0] + '.ktx')
    if filename2[1] == '.ktx':
        os.rename(texturename1[0] + '.ktx', filename2[0] + '.btx')


async def convertprocess_btxtopng(texturename, message: Message):
    texture = pvrpy.PVRTexture(texturename)
    
    if not texture.Decompress(10):
        await message.answer('[Error #310] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)
        
    if texture.SetTextureColourSpace(pvrpy.ColourSpace.sRGB) == False:
        await message.answer('[Error #305] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)
    
    texturename1 = os.path.splitext(texturename)
    if not texture.SaveSurfaceToImageFile(texturename1[0] + ".png"):
        await message.answer('[Error #312] Ошибка при конвертации файла! Перешлите это <b>@nzhasulan</b>')
        os.remove(texturename)
        os.remove(texturename1[0] + ".png")