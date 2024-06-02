import mne
mne.set_log_level("WARNING")
import numpy as np



# Функция для обработки нового блока данных
def process_new_data(raw):

    # Преобразование в numpy массив
    # new_data = np.array(new_data).T
    # Добавление новых данных к уже существующим
    # raw._data = np.hstack((raw._data, new_data))
    # Обновляем время
    # raw._last_samps[-1] += new_data.shape[1]

    # Фильтры обычные
    raw.notch_filter(freqs=50, notch_widths=1)
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
    # raw.notch_filter(freqs=50, notch_widths=1, filter_length='1s', phase='zero')
    # raw.filter(l_freq=0.5, h_freq=30, filter_length='1s', phase='zero')
    # raw.set_eeg_reference(ref_channels='average', projection=True)
    # raw.apply_proj()  # Средняя рефернтная проекция

    data = raw.get_data()

    fft_values = np.fft.fft(data, axis=1)
    freqs = np.fft.fftfreq(data.shape[1], d=1 / raw.info['sfreq'])
    # Частоты
    psd = np.abs(fft_values) ** 2

    waves = {'delta': (0.5, 4),
             'theta': (4, 8),
             'alpha': (8, 12),
             'beta': (12, 30),
             'gamma': (30, 50)}

    max_power_band = None
    max_power = 0
    for band, (low, high) in waves.items():
        band_ix = (freqs >= low) & (freqs < high)
        power = np.mean(psd[:, band_ix], axis=1)
        if np.any(power > max_power):
            max_power = power
            max_power_band = band

    print(max_power_band)
    return max_power_band

if MODE == "INITIALIZATION":
    pass

if MODE == "RUNNING":

    ch_names = ['AF3h', 'AF4h', 'AF5h', 'AF6h', 'AF7', 'AF8', 'AFF1h', 'AFF2h', 'AFF3h', 'AFF4h', 'AFF5h', 'AFF6h', 'AFF7h', 'AFF8h', 'AFp3', 'AFp4', 'AFz', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'CCP1h', 'CCP2h', 'CCP3h', 'CCP4h', 'CCP5h', 'CCP6h', 'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CPP1h', 'CPP2h', 'CPP3h', 'CPP4h', 'CPP5h', 'CPP6h', 'CPz', 'Cz', 'DC-A', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6', 'FCC1h', 'FCC2h', 'FCC3h', 'FCC4h', 'FCC5h', 'FCC6h', 'FCC8h', 'FCz', 'FFC1h', 'FFC2h', 'FFC3h', 'FFC4h', 'FFC5h', 'FFC6h', 'FFT7h', 'FFT8h', 'FPz', 'FT10', 'FT7', 'FT8', 'FT9', 'FTT7h', 'Fp1', 'Fp2', 'Fz', 'I1', 'I2', 'IZ', 'Nz', 'O1', 'O2', 'Oz', 'P1', 'P10', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'PO3h', 'PO4h', 'PO5h', 'PO6h', 'PO7', 'PO8', 'POO3', 'POO4', 'PPO10h', 'PPO1h', 'PPO2h', 'PPO3h', 'PPO4h', 'PPO5h', 'PPO6h', 'PPO7h', 'PPO8h', 'PPO9h', 'Pz', 'T10', 'T7', 'T8', 'T9', 'TP7', 'TP8', 'TPP7h', 'TPP8h', 'TTP7h', 'TTP8h']
    sfreq = 125  # Частота дискретизации
    n_channels = 16  # Количество каналов
    ch_names = ch_names[:n_channels]


    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')

    raw_data = INPUT["EEG In"]
    raw = mne.io.RawArray(raw_data, info)

    OUTPUT["Brain Waves"]=process_new_data(raw)



if MODE == "DESTRUCTION":
    pass

PROCESS()
