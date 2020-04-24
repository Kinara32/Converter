import struct, sys
import numpy as np

##############
# %%  Initialize SEGY HEADER
SH_def = {"Job": {"pos": 3200, "type": "int32", "def": 1}}  # Номер работы
SH_def["Line"] = {"pos": 3204, "type": "int32", "def": 1}  # Номер профиля
SH_def["Reel"] = {"pos": 3208, "type": "int32", "def": 1}  # Номер косы
SH_def["DataTracePerEnsemble"] = {"pos": 3212, "type": "int16", "def": 0}
SH_def["AuxiliaryTracePerEnsemble"] = {"pos": 3214, "type": "int16", "def": 0}
SH_def["dt"] = {"pos": 3216, "type": "uint16", "def": 0}
SH_def["dtOrig"] = {"pos": 3218, "type": "uint16", "def": 1000}
SH_def["ns"] = {"pos": 3220, "type": "uint16", "def": 0}
SH_def["nsOrig"] = {"pos": 3222, "type": "uint16", "def": 0}
SH_def["DataSampleFormat"] = {"pos": 3224, "type": "int16", "def": 5}
SH_def["DataSampleFormat"]["descr"] = {0: {
    1: "IBM Float",
    2: "32 bit Integer",
    3: "16 bit Integer",
    8: "8 bit Integer"}}

SH_def["DataSampleFormat"]["descr"][1] = {
    1: "IBM Float",
    2: "32 bit Integer",
    3: "16 bit Integer",
    5: "IEEE",
    8: "8 bit Integer"}

SH_def["DataSampleFormat"]["bps"] = {0: {
    1: 4,
    2: 4,
    3: 2,
    8: 1}}
SH_def["DataSampleFormat"]["bps"][1] = {
    1: 4,
    2: 4,
    3: 2,
    5: 4,
    8: 1}
SH_def["DataSampleFormat"]["datatype"] = {0: {
    1: 'ibm',
    2: 'l',
    3: 'h',
    8: 'B'}}
SH_def["DataSampleFormat"]["datatype"][1] = {
    1: 'ibm',
    2: 'l',
    3: 'h',
    #    5: 'float',
    5: 'f',
    8: 'B'}

SH_def["EnsembleFold"] = {"pos": 3226, "type": "int16", "def": 1}  #
SH_def["TraceSorting"] = {"pos": 3228, "type": "int16", "def": 1}  #
SH_def["VerticalSumCode"] = {"pos": 3230, "type": "int16", "def": 1}  #
SH_def["SweepFrequencyEnd"] = {"pos": 3234, "type": "int16", "def": 0}
SH_def["SweepLength"] = {"pos": 3236, "type": "int16", "def": 0}
SH_def["SweepType"] = {"pos": 3238, "type": "int16", "def": 0}
SH_def["SweepChannel"] = {"pos": 3240, "type": "int16", "def": 0}
SH_def["SweepTaperlengthStart"] = {"pos": 3242, "type": "int16", "def": 0}
SH_def["SweepTaperLengthEnd"] = {"pos": 3244, "type": "int16", "def": 0}
SH_def["TaperType"] = {"pos": 3246, "type": "int16", "def": 0}
SH_def["CorrelatedDataTraces"] = {"pos": 3248, "type": "int16", "def": 2}  #
SH_def["BinaryGain"] = {"pos": 3250, "type": "int16", "def": 1}  #
SH_def["AmplitudeRecoveryMethod"] = {"pos": 3252, "type": "int16", "def": 1}  # Код метода восстановления амплитуд
SH_def["MeasurementSystem"] = {"pos": 3254, "type": "int16", "def": 1}  # Код метрической системы
SH_def["ImpulseSignalPolarity"] = {"pos": 3256, "type": "int16", "def": 0}
SH_def["VibratoryPolarityCode"] = {"pos": 3258, "type": "int16", "def": 0}
SH_def["Unassigned1"] = {"pos": 3260, "type": "int16", "n": 120, "def": 0}
SH_def["SegyFormatRevisionNumber"] = {"pos": 3500, "type": "uint16", "def": 1}  # Версия сегвая # Не нужно менять
SH_def["FixedLengthTraceFlag"] = {"pos": 3502, "type": "uint16",
                                  "def": 1}  # Если 1, то шаг дискретизации в микросекундах для всего файла одинаковый # Лучше оставить 1
SH_def["NumberOfExtTextualHeaders"] = {"pos": 3504, "type": "uint16", "def": 0}
SH_def["Unassigned2"] = {"pos": 3506, "type": "int16", "n": 47, "def": 0}

##############
# %%  Initialize SEGY TRACE HEADER SPECIFICATION
STH_def = {"TraceSequenceLine": {"pos": 0, "type": "int32"}}
STH_def["TraceSequenceFile"] = {"pos": 4, "type": "int32"}
STH_def["FieldRecord"] = {"pos": 8, "type": "int32"}
STH_def["TraceNumber"] = {"pos": 12, "type": "int32"}
STH_def["EnergySourcePoint"] = {"pos": 16, "type": "int32"}
STH_def["cdp"] = {"pos": 20, "type": "int32"}
STH_def["cdpTrace"] = {"pos": 24, "type": "int32"}
STH_def["TraceIdenitifactionCode"] = {"pos": 28, "type": "uint16", "def": 1}  # 'int16'); % 28
STH_def["TraceIdenitifactionCode"]["descr"] = {0: {
    1: "Seismic data",
    2: "Dead",
    3: "Dummy",
    4: "Time Break",
    5: "Uphole",
    6: "Sweep",
    7: "Timing",
    8: "Water Break"}}
STH_def["TraceIdenitifactionCode"]["descr"][1] = {
    -1: "Other",
    0: "Unknown",
    1: "Seismic data",
    2: "Dead",
    3: "Dummy",
    4: "Time break",
    5: "Uphole",
    6: "Sweep",
    7: "Timing",
    8: "Waterbreak",
    9: "Near-field gun signature",
    10: "Far-field gun signature",
    11: "Seismic pressure sensor",
    12: "Multicomponent seismic sensor - Vertical component",
    13: "Multicomponent seismic sensor - Cross-line component",
    14: "Multicomponent seismic sensor - In-line component",
    15: "Rotated multicomponent seismic sensor - Vertical component",
    16: "Rotated multicomponent seismic sensor - Transverse component",
    17: "Rotated multicomponent seismic sensor - Radial component",
    18: "Vibrator reaction mass",
    19: "Vibrator baseplate",
    20: "Vibrator estimated ground force",
    21: "Vibrator reference",
    22: "Time-velocity pairs"}
STH_def["NSummedTraces"] = {"pos": 30, "type": "int16"}  # 'int16'); % 30
STH_def["NStackedTraces"] = {"pos": 32, "type": "int16"}  # 'int16'); % 32
STH_def["DataUse"] = {"pos": 34, "type": "int16"}  # 'int16'); % 34
STH_def["DataUse"]["descr"] = {0: {
    1: "Production",
    2: "Test"}}
STH_def["DataUse"]["descr"][1] = STH_def["DataUse"]["descr"][0]
STH_def["offset"] = {"pos": 36, "type": "int32", "def": 0}  # Отдаление источника от приемника
STH_def["ReceiverGroupElevation"] = {"pos": 40, "type": "int32"}  # 'int32');             %40
STH_def["SourceSurfaceElevation"] = {"pos": 44, "type": "int32"}  # 'int32');             %44
STH_def["SourceDepth"] = {"pos": 48, "type": "int32"}  # 'int32');             %48
STH_def["ReceiverDatumElevation"] = {"pos": 52, "type": "int32"}  # 'int32');             %52
STH_def["SourceDatumElevation"] = {"pos": 56, "type": "int32"}  # 'int32');             %56
STH_def["SourceWaterDepth"] = {"pos": 60, "type": "int32", "def": 0}  # Глубина воды под источником
STH_def["GroupWaterDepth"] = {"pos": 64, "type": "int32"}  # 'int32');  %64
STH_def["ElevationScalar"] = {"pos": 68, "type": "int16", "def": 1}  # 'int16');  %68
STH_def["SourceGroupScalar"] = {"pos": 70, "type": "int16", "def": 1}  # 'int16');  %70
STH_def["SourceX"] = {"pos": 72, "type": "int32", "def": 0}  # Координаты источника
STH_def["SourceY"] = {"pos": 76, "type": "int32", "def": 0}  # Координаты источника
STH_def["GroupX"] = {"pos": 80, "type": "int32", "def": 0}  # Координаты приемника
STH_def["GroupY"] = {"pos": 84, "type": "int32", "def": 0}  # Координаты приемника
STH_def["CoordinateUnits"] = {"pos": 88, "type": "int16", "def": 1}  # 'int16');  %88
STH_def["CoordinateUnits"]["descr"] = {1: {
    1: "Length (meters or feet)",
    2: "Seconds of arc"}}
STH_def["CoordinateUnits"]["descr"][1] = {
    1: "Length (meters or feet)",
    2: "Seconds of arc",
    3: "Decimal degrees",
    4: "Degrees, minutes, seconds (DMS)"}
STH_def["WeatheringVelocity"] = {"pos": 90, "type": "int16"}  # 'int16');  %90
STH_def["SubWeatheringVelocity"] = {"pos": 92, "type": "int16"}  # 'int16');  %92
STH_def["SourceUpholeTime"] = {"pos": 94, "type": "int16"}  # 'int16');  %94
STH_def["GroupUpholeTime"] = {"pos": 96, "type": "int16"}  # 'int16');  %96
STH_def["SourceStaticCorrection"] = {"pos": 98, "type": "int16"}  # 'int16');  %98
STH_def["GroupStaticCorrection"] = {"pos": 100, "type": "int16"}  # 'int16');  %100
STH_def["TotalStaticApplied"] = {"pos": 102, "type": "int16"}  # 'int16');  %102
STH_def["LagTimeA"] = {"pos": 104, "type": "int16"}  # 'int16');  %104
STH_def["LagTimeB"] = {"pos": 106, "type": "int16"}  # 'int16');  %106
STH_def["DelayRecordingTime"] = {"pos": 108, "type": "int16", "def": 0}  # Время задержки источника
STH_def["MuteTimeStart"] = {"pos": 110, "type": "int16"}  # 'int16');  %110
STH_def["MuteTimeEND"] = {"pos": 112, "type": "int16"}  # 'int16');  %112
STH_def["ns"] = {"pos": 114, "type": "uint16"}  # Число отсчетов в трассе
STH_def["dt"] = {"pos": 116, "type": "uint16", "def": 0}  # Шаг дискретизации
STH_def["GainType"] = {"pos": 119, "type": "int16", "def": 0}  # Режим усиления
STH_def["GainType"]["descr"] = {0: {
    1: "Fixes",
    2: "Binary",
    3: "Floating point"}}
STH_def["GainType"]["descr"][1] = STH_def["GainType"]["descr"][0]
STH_def["InstrumentGainConstant"] = {"pos": 120, "type": "int16"}  # 'int16');  %120
STH_def["InstrumentInitialGain"] = {"pos": 122, "type": "int16"}  # 'int16');  %%122
STH_def["Correlated"] = {"pos": 124, "type": "int16"}  # 'int16');  %124
STH_def["Correlated"]["descr"] = {0: {
    1: "No",
    2: "Yes"}}
STH_def["Correlated"]["descr"][1] = STH_def["Correlated"]["descr"][0]

STH_def["SweepFrequenceStart"] = {"pos": 126, "type": "int16"}  # 'int16');  %126
STH_def["SweepFrequenceEnd"] = {"pos": 128, "type": "int16"}  # 'int16');  %128
STH_def["SweepLength"] = {"pos": 130, "type": "int16"}  # 'int16');  %130
STH_def["SweepType"] = {"pos": 132, "type": "int16"}  # 'int16');  %132
STH_def["SweepType"]["descr"] = {0: {
    1: "linear",
    2: "parabolic",
    3: "exponential",
    4: "other"}}
STH_def["SweepType"]["descr"][1] = STH_def["SweepType"]["descr"][0]

STH_def["SweepTraceTaperLengthStart"] = {"pos": 134, "type": "int16"}  # 'int16');  %134
STH_def["SweepTraceTaperLengthEnd"] = {"pos": 136, "type": "int16"}  # 'int16');  %136
STH_def["TaperType"] = {"pos": 138, "type": "int16"}  # 'int16');  %138
STH_def["TaperType"]["descr"] = {0: {
    1: "linear",
    2: "cos2c",
    3: "other"}}
STH_def["TaperType"]["descr"][1] = STH_def["TaperType"]["descr"][0]

STH_def["AliasFilterFrequency"] = {"pos": 140, "type": "int16"}  # 'int16');  %140
STH_def["AliasFilterSlope"] = {"pos": 142, "type": "int16"}  # 'int16');  %142
STH_def["NotchFilterFrequency"] = {"pos": 144, "type": "int16"}  # 'int16');  %144
STH_def["NotchFilterSlope"] = {"pos": 146, "type": "int16"}  # 'int16');  %146
STH_def["LowCutFrequency"] = {"pos": 148, "type": "int16"}  # 'int16');  %148
STH_def["HighCutFrequency"] = {"pos": 150, "type": "int16"}  # 'int16');  %150
STH_def["LowCutSlope"] = {"pos": 152, "type": "int16"}  # 'int16');  %152
STH_def["HighCutSlope"] = {"pos": 154, "type": "int16"}  # 'int16');  %154
STH_def["YearDataRecorded"] = {"pos": 156, "type": "int16", "def": 2019}  # Год
STH_def["DayOfYear"] = {"pos": 158, "type": "int16", "def": 0}  # День
STH_def["HourOfDay"] = {"pos": 160, "type": "int16", "def": 0}  # Час
STH_def["MinuteOfHour"] = {"pos": 162, "type": "int16", "def": 0}  # Минута
STH_def["SecondOfMinute"] = {"pos": 164, "type": "int16", "def": 0}  # Секунда
STH_def["TimeBaseCode"] = {"pos": 166, "type": "int16", "def": 4}  # Часовой пояс
STH_def["TimeBaseCode"]["descr"] = {0: {
    1: "Local",
    2: "GMT",
    3: "Other"}}
STH_def["TimeBaseCode"]["descr"][1] = {
    1: "Local",
    2: "GMT",
    3: "Other",
    4: "UTC"}
STH_def["TraceWeightningFactor"] = {"pos": 168, "type": "int16",
                                    "def": 0}  # Весовой множитель трассы, определенный как 1/2N Вольт для последнего значащего бита (если есть или 0)
STH_def["GeophoneGroupNumberRoll1"] = {"pos": 170, "type": "int16"}  # 'int16');  %172
STH_def["GeophoneGroupNumberFirstTraceOrigField"] = {"pos": 172, "type": "int16"}  # 'int16');  %174
STH_def["GeophoneGroupNumberLastTraceOrigField"] = {"pos": 174, "type": "int16"}  # 'int16');  %176
STH_def["GapSize"] = {"pos": 176, "type": "int16"}  # 'int16');  %178
STH_def["OverTravel"] = {"pos": 178, "type": "int16"}  # 'int16');  %178
STH_def["OverTravel"]["descr"] = {0: {
    1: "down (or behind)",
    2: "up (or ahead)",
    3: "other"}}
STH_def["OverTravel"]["descr"][1] = STH_def["OverTravel"]["descr"][0]

STH_def["cdpX"] = {"pos": 180, "type": "int32"}  # 'int32');  %180
STH_def["cdpY"] = {"pos": 184, "type": "int32"}  # 'int32');  %184
STH_def["Inline3D"] = {"pos": 188, "type": "int32"}  # 'int32');  %188
STH_def["Crossline3D"] = {"pos": 192, "type": "int32"}  # 'int32');  %192
STH_def["ShotPoint"] = {"pos": 192, "type": "int32"}  # 'int32');  %196
STH_def["ShotPointScalar"] = {"pos": 200, "type": "int16"}  # 'int16');  %200
STH_def["TraceValueMeasurementUnit"] = {"pos": 202, "type": "int16"}  # 'int16');  %202
STH_def["TraceValueMeasurementUnit"]["descr"] = {1: {
    -1: "Other",
    0: "Unknown (should be described in Data Sample Measurement Units Stanza) ",
    1: "Pascal (Pa)",
    2: "Volts (V)",
    3: "Millivolts (v)",
    4: "Amperes (A)",
    5: "Meters (m)",
    6: "Meters Per Second (m/s)",
    7: "Meters Per Second squared (m/&s2)Other",
    8: "Newton (N)",
    9: "Watt (W)"}}
STH_def["TransductionConstantMantissa"] = {"pos": 204, "type": "int32"}  # 'int32');  %204
STH_def["TransductionConstantPower"] = {"pos": 208, "type": "int16"}  # 'int16'); %208
STH_def["TransductionUnit"] = {"pos": 210, "type": "int16"}  # 'int16');  %210
STH_def["TransductionUnit"]["descr"] = STH_def["TraceValueMeasurementUnit"]["descr"]
STH_def["TraceIdentifier"] = {"pos": 212, "type": "int16"}  # 'int16');  %212
STH_def["ScalarTraceHeader"] = {"pos": 214, "type": "int16"}  # 'int16');  %214
STH_def["SourceType"] = {"pos": 216, "type": "int16"}  # 'int16');  %216
STH_def["SourceType"]["descr"] = {1: {
    -1: "Other (should be described in Source Type/Orientation stanza)",
    0: "Unknown",
    1: "Vibratory - Vertical orientation",
    2: "Vibratory - Cross-line orientation",
    3: "Vibratory - In-line orientation",
    4: "Impulsive - Vertical orientation",
    5: "Impulsive - Cross-line orientation",
    6: "Impulsive - In-line orientation",
    7: "Distributed Impulsive - Vertical orientation",
    8: "Distributed Impulsive - Cross-line orientation",
    9: "Distributed Impulsive - In-line orientation"}}

STH_def["SourceEnergyDirectionMantissa"] = {"pos": 218, "type": "int32"}  # 'int32');  %218
STH_def["SourceEnergyDirectionExponent"] = {"pos": 222, "type": "int16"}  # 'int16');  %222
STH_def["SourceMeasurementMantissa"] = {"pos": 224, "type": "int32"}  # 'int32');  %224
STH_def["SourceMeasurementExponent"] = {"pos": 228, "type": "int16"}  # 'int16');  %228
STH_def["SourceMeasurementUnit"] = {"pos": 230, "type": "int16"}  # 'int16');  %230
STH_def["SourceMeasurementUnit"]["descr"] = {1: {
    -1: "Other (should be described in Source Measurement Unit stanza)",
    0: "Unknown",
    1: "Joule (J)",
    2: "Kilowatt (kW)",
    3: "Pascal (Pa)",
    4: "Bar (Bar)",
    4: "Bar-meter (Bar-m)",
    5: "Newton (N)",
    6: "Kilograms (kg)"}}
STH_def["UnassignedInt1"] = {"pos": 232, "type": "int32"}  # 'int32');  %232
STH_def["UnassignedInt2"] = {"pos": 236, "type": "int32"}  # 'int32');  %236


def getDefaultSegyHeader(numsensors, numsensors_nonzero, ntraces, ns, dt, Job, Line, Reel, sensorsAll):
    """
    SH=getDefaultSegyHeader()
    """
    # INITIALIZE DICTIONARY
    SH = {"Job": {"pos": 3200, "type": "int32", "def": 0}}

    for key in SH_def.keys():

        tmpkey = SH_def[key]

        if 'def' in tmpkey:
            val = tmpkey['def']
        else:
            val = 0
        SH[key] = val

    SH["ntraces"] = ntraces
    SH["ns"] = ns
    SH["dt"] = dt
    SH["Job"] = Job  # Номер работы
    SH["Line"] = Line  # Номер профиля
    SH["Reel"] = Reel  # Номер косы

    if sensorsAll == 1:
        SH["DataTracePerEnsemble"] = numsensors  # Количество датчиков
    else:
        SH["DataTracePerEnsemble"] = numsensors_nonzero  # Номер датчика для построения
    return SH


def getDefaultGPSData(filename, readAll, pack_in, size):
    PacType_list = []
    Longitude_list = []
    Latitude_list = []
    GreenwichTime_list = []
    Status_list = []
    NS_list = []
    EW_list = []
    Speed_list = []
    Direction_list = []
    Date_list = []
    Mode_list = []
    Check_sum_list = []

    # if readAll == 1:
    #     with open(filename, 'rb') as Data:
    #         AllData = Data.read()
    #         filesize = len(AllData)
    #         numpackage = int(filesize / size)  # Количество пакетов в записи # Должно быть кратно и не меньше ns
    # else:
    #     numpackage = pack_in

    with open(filename, 'rb') as Data:
        # for package in range (numpackage):
        while True:

            while True:

                getbyte1 = Data.read(1)
                print(getbyte1)
                PacType_list.append(getbyte1)
                if getbyte1 == b'$':
                    getbyte2 = Data.read(1)
                    print(getbyte2)
                    if getbyte2 == b'G':
                        getbyte3 = Data.read(1)
                        print(getbyte3)
                        if getbyte3 == b'P':
                            getbyte4 = Data.read(1)
                            print(getbyte4)
                            if getbyte4 == b'R':
                                getbyte5 = Data.read(1)
                                print(getbyte5)
                                if getbyte5 == b'M':
                                    getbyte6 = Data.read(1)
                                    print(getbyte6)
                                    if getbyte6 == b'C':
                                        break
                elif getbyte1 == b'':
                    break

            if getbyte1 == b'':
                 break

            Separator = Data.read(1)
            GreenwichTime = Data.read(9)
            Separator = Data.read(1)
            Status = Data.read(1)
            Separator = Data.read(1)
            Latitude = Data.read(9)
            Separator = Data.read(1)
            NS = Data.read(1)
            Separator = Data.read(1)
            Longitude = Data.read(10)
            Separator = Data.read(1)
            EW = Data.read(1)
            Separator = Data.read(1)
            Speed = Data.read(5)
            Separator = Data.read(1)
            Direction = Data.read(5)
            Separator = Data.read(1)
            Date = Data.read(6)
            Separator = Data.read(3)
            Mode = Data.read(1)
            Separator = Data.read(1)
            Check_sum = Data.read(2)
            # Zero = Data.read(31)

            # PacType_list.append(PacType)
            GreenwichTime_list.append(GreenwichTime)
            Status_list.append(Status)
            NS_list.append(NS)
            Longitude_list.append(Longitude)
            Latitude_list.append(Latitude)
            EW_list.append(EW)
            Speed_list.append(Speed)
            Direction_list.append(Direction)
            Date_list.append(Date)
            Mode_list.append(Mode)
            Check_sum_list.append(Check_sum)


    a = len(Longitude_list)
    aa = len (Latitude_list)

    return Longitude_list, Latitude_list


# %%
def getDefaultSegyTraceHeaders(numsensors, numsensors_nonzero, distance, ntraces, ns, dt, offset, SourceWaterDepth,
                               SourceX, SourceY,
                               GroupX,
                               GroupY, Day, sensorsAll):  # Day,
    # Year, Hour, Minute, Second):
    """
    STH=getDefaultSegyTraceHeader()
    """
    # INITIALIZE DICTIONARY
    STH = {"TraceSequenceLine": {"pos": 0, "type": "int32"}}

    for key in STH_def.keys():

        tmpkey = STH_def[key]

        if 'def' in tmpkey:
            val = tmpkey['def']
        else:
            val = 0
        STH[key] = np.tile(val, (ntraces))

    for a in range(ntraces):
        STH["TraceSequenceLine"][a] = a + 1
        STH["TraceSequenceFile"][a] = a + 1
        STH["FieldRecord"][a] = 1000
        STH["ns"][a] = ns
        STH["dt"][a] = dt
        STH["SourceWaterDepth"][a] = SourceWaterDepth  # Глубина воды под источником
        STH["SourceX"][a] = SourceX  # Координаты источника
        STH["SourceY"][a] = SourceY  # Координаты источника
        STH["GroupX"][a] = GroupX  # Координаты приемника
        STH["GroupY"][a] = GroupY  # Координаты приемника
        STH["DayOfYear"][a] = Day  # День

    if sensorsAll == 1:

        numparts = int(ntraces / numsensors)
        numsensors_arr = np.arange(1, numsensors + 1)
        offset_arr = np.arange(offset, (distance * numsensors + offset), distance)
        STH["TraceNumber"] = np.tile(numsensors_arr, numparts)  # Номер датчика для трассы
        STH["offset"] = np.tile(offset_arr, numparts)  # Отдаление источника от приемника

    else:

        for a in range(ntraces):
            STH["TraceNumber"][a] = numsensors_nonzero  # Номер датчика для трассы
            STH["offset"][a] = distance * numsensors_nonzero + offset  # Отдаление источника от приемника

    return STH


def getDefaultSegyDataBin(filename_bin, filename_cannon, numsensors, numsensors_nonzero, ns, pack_in, sizeCanon,
                          format, readAll,
                          sortFlag, delay, sensorAll):
    NumPacCannon = getDefaultCanonData(filename_cannon, sizeCanon, readAll, pack_in)
    numparts = len(NumPacCannon)  # Количество частей записи

    NumPac_list = []

    if sensorAll == 0:
        ntraces = numparts - 1
    else:
        ntraces = numsensors * (numparts - 1)  # Количество трасс

    with open(filename_bin, 'rb') as Data:

        Data_trace = np.zeros((1, 1), dtype=np.float32)
        Data_ns = np.zeros((1, numsensors + 1), dtype=np.float32)
        Data_seg = np.zeros((ns + 1, 1), dtype=np.float32)
        Time_zero = np.zeros((1, 1), dtype=np.float32)

        for part in range(numparts - 1):

            while True:

                Header = Data.read(4)
                Header2 = Data.read(6)
                NumPac = Data.read(6)
                Day = Data.read(1)
                Month = Data.read(1)
                Year = Data.read(1)
                Hour = Data.read(1)
                Minute = Data.read(1)
                Second = Data.read(1)
                Hundreds_of_microseconds = Data.read(2)

                for isensor in range(numsensors):
                    SensorData = Data.read(4)

                NumPac_int = int.from_bytes(NumPac, byteorder='big')
                # NumPac_list.append(NumPac_int)
                # print("Kosa: " + str(NumPac_int))
                # print("Cannon: " + str(NumPacCannon[part]))

                if NumPac_int >= (NumPacCannon[part] + delay):
                    break

            for s in range(ns):

                Header = Data.read(10)
                NumPac = Data.read(6)
                Day = Data.read(1)
                Month = Data.read(1)
                Year = Data.read(1)
                Hour = Data.read(1)
                Minute = Data.read(1)
                Second = Data.read(1)
                Hundreds_of_microseconds = Data.read(2)

                for isensor in range(numsensors):
                    SensorData = Data.read(4)
                    strVal = struct.unpack(format, SensorData)
                    Data_arr = np.array(strVal, dtype=np.float32).reshape(1, 1)
                    Data_trace = np.concatenate((Data_trace, Data_arr), axis=1)

                Data_ns = np.concatenate((Data_ns, Data_trace), axis=0)
                Data_trace = np.zeros((1, 1), dtype=np.float32)

                printverbose('Data preparation #' + str(s + 1) + '/' + str(ns), 20)

            if sensorAll == 0:
                ntraces = numparts - 1
                Data_without_zero = np.hsplit(Data_ns, (numsensors_nonzero, numsensors_nonzero + 1))
                # Data_without_zero.pop(2)
                # Data_without_zero.pop(1)
                Data_ns = Data_without_zero[1]
                sortFlag = 2

            if sortFlag == 0:

                Data_seg = np.concatenate((Data_seg, Data_ns), axis=1)
                Data_seg = np.delete(Data_seg, (part * numsensors_nonzero + 1), 1)
                printverbose('Data preparation #' + str(part + 1) + '/' + str(numparts), 10)
                Data_ns = np.zeros((1, numsensors + 1), dtype=np.float32)

            elif sortFlag == 2:

                Data_seg = np.concatenate((Data_seg, Data_ns), axis=1)
                printverbose('Data preparation #' + str(part + 1) + '/' + str(numparts), 10)
                Data_ns = np.zeros((1, numsensors + 1), dtype=np.float32)

            else:
                part16_list = np.hsplit(Data_ns, (16, 17))
                part16 = np.concatenate((part16_list[0], part16_list[1]), axis=1)
                part16 = np.delete(part16, 0, 1)

                part32_list = np.hsplit(part16_list[2], (15, 16))
                part32 = np.concatenate((part32_list[0], part32_list[1]), axis=1)

                part48_list = np.hsplit(part32_list[2], (15, 16))
                part48 = np.concatenate((part48_list[0], part48_list[1]), axis=1)

                part64_list = np.hsplit(part48_list[2], (15, 16))
                part64 = np.concatenate((part64_list[0], part64_list[1]), axis=1) * (-1)

                part80_list = np.hsplit(part64_list[2], (15, 16))
                part80 = np.concatenate((part80_list[0], part80_list[1]), axis=1)
                part96 = part80_list[2] * (-1)

                #####################################################################
                Data_sort = np.concatenate((part48, part16), axis=1)  # 1-16 + 17-32
                Data_sort = np.concatenate((Data_sort, part32), axis=1)  # 17-32 + 33-48
                Data_sort = np.concatenate((Data_sort, part96), axis=1)  # 33-48 + 49-64
                Data_sort = np.concatenate((Data_sort, part64), axis=1)  # 49-64 + 65-80
                Data_sort = np.concatenate((Data_sort, part80), axis=1)  # 65-80 + 80-96

                Data_seg = np.concatenate((Data_seg, Data_sort), axis=1)
                printverbose('Data preparation #' + str(part + 1) + '/' + str(numparts), 10)
                Data_ns = np.zeros((1, numsensors + 1), dtype=np.float32)

        Data_seg = np.delete(Data_seg, 0, 0)
        Data_seg = np.delete(Data_seg, 0, 1)

    return Data_seg, ntraces


def getDefaultCanonData(filename_cannon, sizeCanon, readAll, pack_in):
    NumPacCannon_list = []

    if readAll == 1:
        with open(filename_cannon, 'rb') as Data:
            AllData = Data.read()
            filesize = len(AllData)
            numpackage = int(filesize / sizeCanon)  # Количество пакетов в записи # Должно быть кратно и не меньше ns
    else:
        numpackage = pack_in

    with open(filename_cannon, 'rb') as CannonData:
        for package in range(numpackage):
            HeaderCannon = CannonData.read(4)
            HeaderCannon2 = CannonData.read(2)
            NumPacCannon = CannonData.read(6)
            DayCannon = CannonData.read(1)
            MonthCannon = CannonData.read(1)
            YearCannon = CannonData.read(1)
            HourCannon = CannonData.read(1)
            MinuteCannon = CannonData.read(1)
            SecondCannon = CannonData.read(1)
            Hundreds_of_microseconds_Cannon = CannonData.read(2)
            N = CannonData.read(1)
            Period = CannonData.read(3)
            Delay = CannonData.read(2)
            Others = CannonData.read(94)

            NumPacCannon_int = int.from_bytes(NumPacCannon, byteorder='big')

            NumPacCannon_list.append(NumPacCannon_int)
    return NumPacCannon_list


# %%
def getDefaultSegyDataTxt(filename_txt, numsensors, numsensors_real, ns, txt_str):
    #
    # Data = getDefaultSegyData(filename_txt, numsensors, numsensors_real, ns, numparts)
    #
    numparts = int(txt_str / ns)

    with open(filename_txt, 'r') as Data:
        Data_str = Data.read()

    Data_list = Data_str.split()
    Data_arr = np.array(Data_list, dtype=np.float32).reshape(txt_str, numsensors)

    if numsensors == numsensors_real:

        Data_seg = Data_arr[0:ns:1]

        for i in range(numparts - 1):
            Data_parts = Data_arr[ns * (i + 1):ns * (i + 2):1]
            Data_seg = np.concatenate((Data_seg, Data_parts), axis=1)

    elif numsensors != numsensors_real:

        Data_without_zero = np.hsplit(Data_arr, (numsensors_real, numsensors_real + 1))
        Data_without_zero.pop(2)
        Data_without_zero.pop(1)
        Data_seg = Data_without_zero[0][0:ns:1]

        for i in range(numparts - 1):
            Data_parts = Data_without_zero[0][ns * (i + 1):ns * (i + 2):1]
            Data_seg = np.concatenate((Data_seg, Data_parts), axis=1)

    return Data_seg


# endian='>' # Big Endian  # modified by A Squelch
# endian='<' # Little Endian
# endian='=' # Native

l_int = struct.calcsize('i')
l_uint = struct.calcsize('I')
l_long = struct.calcsize('l')

l_ulong = struct.calcsize('L')
l_short = struct.calcsize('h')
l_ushort = struct.calcsize('H')
l_char = struct.calcsize('c')
l_uchar = struct.calcsize('B')
l_float = struct.calcsize('f')


# %%
def writeSegyStructure(filename, Data, TH, SH, STH, endian='>'):  # modified by A Squelch
    """
    writeSegyStructure(filename,Data,SegyHeader,SegyTraceHeaders)

    Write SEGY file

    """

    printverbose("writeSegyStructure : Trying to write " + filename, 0)

    with open(filename, 'wb') as f:

        # VERBOSE INF
        revision = SH["SegyFormatRevisionNumber"]
        dsf = SH["DataSampleFormat"]

        try:  # block added by A Squelch
            DataDescr = SH_def["DataSampleFormat"]["descr"][revision][dsf]
        except KeyError:
            print("")
            print("  An error has ocurred interpreting a SEGY binary header key")
            print("  Please check the Endian setting for this file: ", filename)
            sys.exit()

        printverbose("writeSegyStructure : SEG-Y revision = " + str(revision), 1)
        printverbose("writeSegyStructure : DataSampleFormat=" + str(dsf) + "(" + DataDescr + ")", 1)

        # WRITE TEXT HEADER

        f.write(TH.encode('ascii'))

        # WRITE SEGY HEADER

        for key in SH_def.keys():
            pos = SH_def[key]["pos"]
            format = SH_def[key]["type"]
            value = SH[key]

            putValue(value, f, pos, format, endian)

            txt = str(pos) + " " + str(format) + "  Reading " + key + "=" + str(value)
            printverbose(txt, 40)

        # SEGY TRACES

        ctype = SH_def['DataSampleFormat']['datatype'][revision][dsf]
        bps = SH_def['DataSampleFormat']['bps'][revision][dsf]

        sizeT = 240 + SH['ns'] * bps

        for itrace in range(SH['ntraces']):
            index = 3600 + itrace * sizeT
            printverbose('Writing Trace #' + str(itrace + 1) + '/' + str(SH['ntraces']), 10)
            # WRITE SEGY TRACE HEADER
            for key in STH_def.keys():
                pos = index + STH_def[key]["pos"]
                format = STH_def[key]["type"]
                value = STH[key][itrace]
                txt = str(pos) + " " + str(format) + "  Writing " + key + "=" + str(value)

                printverbose(txt, 30)
                putValue(value, f, pos, format, endian)

                # WRITE DATA
            cformat = endian + ctype

            for s in range(SH['ns']):
                strVal = struct.pack(cformat, Data[s, itrace])
                f.seek(index + 240 + s * struct.calcsize(cformat))
                f.write(strVal)


# %%
def putValue(value, fileid, index, ctype='l', endian='>', number=1):
    """
    putValue(data,index,ctype,endian,number)
    """
    if (ctype == 'l') | (ctype == 'long') | (ctype == 'int32'):
        size = l_long
        ctype = 'l'
        value = int(value)
    elif (ctype == 'L') | (ctype == 'ulong') | (ctype == 'uint32'):
        size = l_ulong
        ctype = 'L'
        value = int(value)
    elif (ctype == 'h') | (ctype == 'short') | (ctype == 'int16'):
        size = l_short
        ctype = 'h'
        value = int(value)
    elif (ctype == 'H') | (ctype == 'ushort') | (ctype == 'uint16'):
        size = l_ushort
        ctype = 'H'
        value = int(value)
    elif (ctype == 'c') | (ctype == 'char'):
        size = l_char
        ctype = 'c'
    elif (ctype == 'B') | (ctype == 'uchar'):
        size = l_uchar
        ctype = 'B'
    elif (ctype == 'f') | (ctype == 'float'):
        size = l_float
        ctype = 'f'
    elif (ctype == 'ibm'):
        size = l_float
    else:
        printverbose('Bad Ctype : ' + ctype, -1)

    cformat = endian + ctype * number

    printverbose('cformat="%s", ctype="%s", value=%f' % (cformat, ctype, value), 40)
    strVal = struct.pack(cformat, value)
    fileid.seek(index)
    fileid.write(strVal)

    return 1


verbose = 10


# %%
def printverbose(txt, level=1):
    if level <= verbose:
        print(txt)
