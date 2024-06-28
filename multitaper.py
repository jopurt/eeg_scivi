import mne
mne.set_log_level("WARNING")
import numpy as np
from mne.preprocessing import ICA, create_eog_epochs, create_ecg_epochs
from mne.time_frequency import psd_array_multitaper
from scipy.signal import welch

# Функция для обработки нового блока данных
def process_new_data(raw):

    # Преобразование в numpy массив
    # new_data = np.array(new_data).T
    # Добавление новых данных к уже существующим
    # raw._data = np.hstack((raw._data, new_data))
    # Обновляем время
    # raw._last_samps[-1] += new_data.shape[1]

    # Фильтры обычные
    # raw.notch_filter(freqs=50, notch_widths=1)
    # raw.filter(l_freq=0.5, h_freq=30)
    # raw.set_eeg_reference(ref_channels='average', projection=True)
    # raw.apply_proj()  # Средняя рефернтная проекция


    # Создание событий для разделения на эпохи по 1 секунде
    #events = mne.make_fixed_length_events(raw, duration=1.0)

    # Создание эпох
    #epochs = mne.Epochs(raw, events, tmin=0, tmax=1, baseline=None, preload=True)

    #wave_types = []

    #--------------------
    # Получение данных для текущей секунды
    #epoch_data = epochs[i].get_data(copy=True)[0]

    # Попробовать фильтры поменьше
    # raw.notch_filter(freqs=50, notch_widths=1, filter_length='8s', phase='zero')
    # raw.filter(l_freq=0.5, h_freq=30, filter_length='8s', phase='zero')
    # raw.set_eeg_reference(ref_channels='average', projection=True)
    # raw.apply_proj()  # Средняя рефернтная проекция
    #----------------------------------------------------------------------------------------------------------------------
    max_buffer_size = int(raw.info['sfreq'] * 7)  # 7 секунд данных

    # инициализация буфера из кэша
    if "eeg_buffer" not in CACHE:
        CACHE["eeg_buffer"] = raw.get_data()
        print("Initializing the buffer.")
    else:
        # текущий буфер
        data_buffer = CACHE["eeg_buffer"]
        new_data = raw.get_data()

        print(f"New data: {new_data.shape}")

        # добавляем новые данные в буфер
        data_buffer = np.hstack((data_buffer, new_data))
        print("Add new data in biffer.")
        print(f"Buffer size after adding new data: {data_buffer.shape}")

        # ограничение размера буфера до 7 секунд
        # max_buffer_size = int(raw.info['sfreq'] * 7)  # 7 секунд данных
        if data_buffer.shape[1] > max_buffer_size:
            data_buffer = data_buffer[:, -max_buffer_size:]
            print("Limit the buffer size to 7 seconds.")

        # Обновляем буфер в кэше
        CACHE["eeg_buffer"] = data_buffer

    # получаем обновленный буфер из кэша
    data_buffer = CACHE["eeg_buffer"]
    print(f"Current buffer size: {data_buffer.shape}")

    # накопилось ли достаточно данных для фильтрации и анализа
    if (data_buffer.shape[1] < max_buffer_size):
        print("There is not enough data to filter and analyze.")
        return "None"  # возвращаем None если данных недостаточно

    # создание RawArray с данными из буфера
    info = raw.info
    buffer_raw = mne.io.RawArray(data_buffer, info)

    # применение фильтров
    buffer_raw.notch_filter(freqs=50, notch_widths=1)
    # buffer_raw.filter(l_freq=0.5, h_freq=None)
    buffer_raw.filter(l_freq=0.5, h_freq=30)
    # buffer_raw.set_eeg_reference(ref_channels='average', projection=True)
    # buffer_raw.apply_proj()  # средняя референтная проекция

    #----------------Доп фильтры-----------------

    # # ICA для удаления артефактов
    # ica = ICA(n_components=20, random_state=97, max_iter=800)
    # ica.fit(buffer_raw)
    #
    # # Найти и удалить EOG артефакты
    # eog_epochs = create_eog_epochs(buffer_raw)
    # eog_inds, _ = ica.find_bads_eog(eog_epochs)
    # ica.exclude.extend(eog_inds)
    #
    # # Найти и удалить ECG артефакты
    # ecg_epochs = create_ecg_epochs(buffer_raw)
    # ecg_inds, _ = ica.find_bads_ecg(ecg_epochs)
    # ica.exclude.extend(ecg_inds)
    #
    # buffer_raw = ica.apply(buffer_raw)

    # ----------------Доп фильтры-----------------

    # ----------------Доп фильтры 2-----------------

    # ica = mne.preprocessing.ICA(
    #     method="picard",
    #     fit_params={"extended": True, "ortho": False},
    #     random_state=1
    # )
    # 
    #
    # ica.fit(buffer_raw)
    #
    # ica.exclude = [1]
    #
    # ica.apply(buffer_raw)


    # ----------------Доп фильтры 2-----------------

    # получение данных
    data = buffer_raw.get_data()

    # FFT
    # fft_values = np.fft.fft(data, axis=1)
    # freqs = np.fft.fftfreq(data.shape[1], d=1 / raw.info['sfreq'])
    # # частоты
    # psd = np.abs(fft_values) ** 2

    # multitaper
    psds, freqs = psd_array_multitaper(data, sfreq=raw.info['sfreq'], fmin=0.5, fmax=50, bandwidth=4.0, verbose=False)
    # Среднее значение PSD по времени
    psds = psds.mean(axis=0)

    # Welch
    # freqs, psds = welch(data, fs=raw.info['sfreq'], nperseg=4 * raw.info['sfreq'])
    
    waves = {'delta': (0.5, 4),
             'theta': (4, 8),
             'alpha': (8, 12),
             'beta': (12, 30),
             'gamma': (30, 50)}

    power_values = {}
    max_power_band = None
    max_power = 0

    #для FFT
    # for band, (low, high) in waves.items():
    #     band_ix = (freqs >= low) & (freqs < high)
    #     power = np.mean(psd[:, band_ix], axis=1)
    #     power_values[band] = power
    #     if np.any(power > max_power):
    #         max_power = power
    #         max_power_band = band

    #для multitaper
    for band, (low, high) in waves.items():
        band_ix = np.logical_and(freqs >= low, freqs < high)
        power = psds[band_ix].mean(axis=0)
        power_values[band] = power
        if power > max_power:
            max_power = power
            max_power_band = band

    #для Welch'a
    # for band, (low, high) in waves.items():
    #     band_ix = np.logical_and(freqs >= low, freqs < high)
    #     power = psds[:, band_ix].mean(axis=1)
    #     power_values[band] = power
    #     if np.any(power > max_power):
    #         max_power = power
    #         max_power_band = band

    # среднее скользящее окно для Welcha'a
    # if "power_cache" not in CACHE:
    #     CACHE["power_cache"] = {band: [] for band in waves}
    #
    # for band, (low, high) in waves.items():
    #     band_ix = np.logical_and(freqs >= low, freqs < high)
    #     power = psds[:, band_ix].mean(axis=1)
    #
    #     # Добавление новых данных в кэш
    #     CACHE["power_cache"][band].append(power)
    #
    #     # Ограничение размера кэша до размера скользящего окна
    #     if len(CACHE["power_cache"][band]) > max_buffer_size:
    #         CACHE["power_cache"][band].pop(0)
    #
    #     # Вычисление среднего значения мощности для текущего диапазона
    #     power_values[band] = np.mean(CACHE["power_cache"][band], axis=0)
    #
    #     if np.any(power_values[band] > max_power):
    #         max_power = power_values[band]
    #         max_power_band = band

    print("--------------")
    for band, power in power_values.items():
        print(f"{band}: {np.mean(power)}")
    print("--------------")
    return max_power_band

if MODE == "INITIALIZATION":
    pass

if MODE == "RUNNING":
    #для EBneuro
    ch_names = ['AF3h', 'AF4h', 'AF5h', 'AF6h', 'AF7', 'AF8', 'AFF1h', 'AFF2h', 'AFF3h', 'AFF4h', 'AFF5h', 'AFF6h', 'AFF7h',
                'AFF8h', 'AFp3', 'AFp4', 'AFz', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'CCP1h', 'CCP2h', 'CCP3h', 'CCP4h', 'CCP5h',
                'CCP6h', 'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CPP1h', 'CPP2h', 'CPP3h', 'CPP4h', 'CPP5h', 'CPP6h', 'CPz',
                'Cz', 'DC-A','DC-B','DC-C','DC-D','DC-E','DC-F','DC-G','DC-H', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6', 'FCC1h',
                'FCC2h', 'FCC3h', 'FCC4h', 'FCC5h', 'FCC6h', 'FCC8h', 'FCz', 'FFC1h', 'FFC2h', 'FFC3h', 'FFC4h', 'FFC5h', 'FFC6h',
                'FFT7h', 'FFT8h', 'FPz', 'FT10', 'FT7', 'FT8', 'FT9', 'FTT7h', 'Fp1', 'Fp2', 'Fz', 'I1', 'I2', 'IZ', 'Nz', 'O1',
                'O2', 'Oz', 'P1', 'P10', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'PO3h', 'PO4h', 'PO5h', 'PO6h', 'PO7',
                'PO8', 'POO3', 'POO4', 'PPO10h', 'PPO1h', 'PPO2h', 'PPO3h', 'PPO4h', 'PPO5h', 'PPO6h', 'PPO7h', 'PPO8h', 'PPO9h',
                'Pz', 'T10', 'T7', 'T8', 'T9', 'TP7', 'TP8', 'TPP7h', 'TPP8h', 'TTP7h', 'TTP8h']

    # ch_names = ['AF3h', 'AF4h', 'AF5h', 'AF6h', 'AF7', 'AF8', 'AFF1h', 'AFF2h', 'AFF3h', 'AFF4h', 'AFF5h', 'AFF6h','AFF7h',
    #             'AFF8h', 'AFp3', 'AFp4', 'AFz', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'CCP1h', 'CCP2h', 'CCP3h', 'CCP4h','CCP5h',
    #             'CCP6h', 'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CPP1h', 'CPP2h', 'CPP3h', 'CPP4h', 'CPP5h', 'CPP6h','CPz',
    #             'Cz', 'DC-A', 'F1', 'F2', 'F3', 'F4', 'F5',
    #             'F6', 'F7', 'F8', 'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6', 'FCC1h',
    #             'FCC2h', 'FCC3h', 'FCC4h', 'FCC5h', 'FCC6h', 'FCC8h', 'FCz', 'FFC1h', 'FFC2h', 'FFC3h', 'FFC4h','FFC5h', 'FFC6h',
    #             'FFT7h', 'FFT8h', 'FPz', 'FT10', 'FT7', 'FT8', 'FT9', 'FTT7h', 'Fp1', 'Fp2', 'Fz', 'I1', 'I2', 'IZ','Nz', 'O1',
    #             'O2', 'Oz', 'P1', 'P10', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'PO3h', 'PO4h', 'PO5h', 'PO6h','PO7',
    #             'PO8', 'POO3', 'POO4', 'PPO10h', 'PPO1h', 'PPO2h', 'PPO3h', 'PPO4h', 'PPO5h', 'PPO6h', 'PPO7h', 'PPO8h','PPO9h',
    #             'Pz', 'T10', 'T7', 'T8', 'T9', 'TP7', 'TP8', 'TPP7h', 'TPP8h', 'TTP7h', 'TTP8h']
    # sfreq = 125  # Частота дискретизации
    sfreq = 512  # Частота дискретизации
    # n_channels = 16  # Количество каналов
    # ch_names = ch_names[:n_channels]

    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')

    #здесь приходит 140 каналов, но надо вырезать 4 канала
    INPUT["EEG In"]=INPUT["EEG In"][:136]
    raw_data = INPUT["EEG In"]
    raw = mne.io.RawArray(raw_data, info)

    #OUTPUT["Brain Waves"]=process_new_data(raw)

    result = process_new_data(raw)
    if result:
        print("$$$$$$$$")
        print(result)
        print("$$$$$$$$")
        OUTPUT["Brain Waves"] = result



if MODE == "DESTRUCTION":
    pass

PROCESS()