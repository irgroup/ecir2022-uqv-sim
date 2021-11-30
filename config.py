import yaml

with open("config/default.yml", "r") as ymlfile:
    default = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("config/qcmcqg_kis_s6.yml", "r") as ymlfile:
    qcmcqg_kis_s6 = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("config/qcmcqg_kis_s7.yml", "r") as ymlfile:
    qcmcqg_kis_s7 = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("config/qcmcqg_kis_s8.yml", "r") as ymlfile:
    qcmcqg_kis_s8 = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("config/qcmcqg_tts_s6.yml", "r") as ymlfile:
    qcmcqg_tts_s6 = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("config/qcmcqg_tts_s7.yml", "r") as ymlfile:
    qcmcqg_tts_s7 = yaml.load(ymlfile, Loader=yaml.FullLoader)

with open("config/qcmcqg_tts_s8.yml", "r") as ymlfile:
    qcmcqg_tts_s8 = yaml.load(ymlfile, Loader=yaml.FullLoader)
