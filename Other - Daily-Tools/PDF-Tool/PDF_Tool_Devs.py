"""
PDF Tool - GUI App
Tkinter-basierte Oberfläche für PDF drehen, komprimieren, zusammenführen
"""

import sys
import os
import threading
from pathlib import Path

def install_requirements():
    import subprocess
    for pkg in ["pymupdf"]:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

try:
    import fitz
except ImportError:
    install_requirements()
    import fitz

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import base64, io

LOGO_B64 = """iVBORw0KGgoAAAANSUhEUgAAAEQAAABGCAYAAAB12zK5AAABCGlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGA8wQAELAYMDLl5JUVB7k4KEZFRCuwPGBiBEAwSk4sLGHADoKpv1yBqL+viUYcLcKakFicD6Q9ArFIEtBxopAiQLZIOYWuA2EkQtg2IXV5SUAJkB4DYRSFBzkB2CpCtkY7ETkJiJxcUgdT3ANk2uTmlyQh3M/Ck5oUGA2kOIJZhKGYIYnBncAL5H6IkfxEDg8VXBgbmCQixpJkMDNtbGRgkbiHEVBYwMPC3MDBsO48QQ4RJQWJRIliIBYiZ0tIYGD4tZ2DgjWRgEL7AwMAVDQsIHG5TALvNnSEfCNMZchhSgSKeDHkMyQx6QJYRgwGDIYMZAKbWPz9HbOBQAAAgMElEQVR4nM2cd5QkyV3nPxGRWVmmq7vaTrvp7ukxOzuzTkJid5FDIMMhuHuAxAl4OPF0AiGd4N4JOOEOTiAd7g5zwkgcSDg97pCEYJ+kXaEVq7Ws0+7szsyO6Z5207aqu6rLZmZE3B+RVd09Zme0u8DFe/W6OrMyzC8ifub7+0aKx++/xwohuFZ5vt8IIbDWur8ChAABWGMx2mCsRSqF8tOk02l83ycVpPFTKaSUnXosFh3HRK0mYRgStkLCqI6OIwCUlEipQAisBWGv3bfrKdbaznfvRdW0uwgnCWkNsTZYa0n5AfmebvKFXrK5bvwgQAiBMQajNXEcY4zBYpMqBJ7yUJ6HUgohBDqOadZr1CpbVCtbNJp1rNEoKRFSYa/Rrevr+o5APaAzu9fzwNWuC+tmV3o+Pb399A7uI5fvRUhBq1GjUqnQrFVoNptEUQQ6xBgN1olDuAoRQiA8D8/zCIIU6UwPue4CA6MT7Js4SNiss1Vcp1xcp9WsI6REKrVnll+UcB6//x77fIO+0j0rAAtSuC9aR0gvTd/AMEMjY3i+R217m83SBtXyJlGrAdaAFEihEEJ2tlYiip2/1iKwWOsewUYgQKoU6a48hb4BCr39KOVT2SqxtrxEo1ZGCoGUEtup74UJSDzxwBev+eRlwhIWgUBrjRAevftGGB0dAyTF4jql9RVa9RoCg1TK7fvkOddPgcXgFMGu/gsQiKQ9gUAmw7JYa7FGY41FpgLyhT6GhsfJZDNslYqsLs3RqldRvn9d8miPaffusNZeWyCXrxwBaGKtyff0s3/qEKkgy9ryIhurF4nDBkpJhJDu2UThWmMwGLDC3VOqoyd2j0BrjdUGa40TvJBIIXcpX4u1Bm1iEB75nn6GxybJZNOsLi+wtrwERqOk94K20dckECFwClF4jE5MsG94P6XiBivz52m1GnhKIMSOnjbGKVepFEE6Q9DVTTaTJZ3O4KUCPM/fGah1govjiDgOaTUbNJo1mtVtWo0GRscICVIJQCb7VqO1E1rv4Agj+yeJwybzM+dpVMt4avcWegkEslcYAhOHeOkuDtxwE0EQMD9zmq3SOkqoZGBOQRptQAgy2Rw9vf3kC32ks3k8z/+aOgdgraHVqFEtlyhvFqnVKlhrnZXBbS1rLbGOSQUZxqYO013oY+nCOUqrC0jPS4TXHgfskdGue4hrbJkdgQiMNuS6ezl49CYatQqz508Shi18T4KVCCRaW8DQ1dNL//AY3T0FPC8FgLEkyjIxsZ3eXUkIO2YYIXapGUO1Uqa4dpHtzSJGG5SnAIsEjLZYKxgY2c/I5AE2VpdYnp9BsMuKikuGe4lArumHCCGIo4j8wDAHj9xIcX2FxfNnkcKSUn5iNi1xrOnK9TA4PkFPfz9SSIy1xMYgRXtSxPNas72T0P6eeCkWEJJ8dy/57gLV7TIbSwtUyhsIabFCIZRAIlhbvkCjsc3UkeOk/ID58ycTBS65VNte6nJccYUIIVz7QqAjTWFwH9OHb2BpaY6V+Tn8XcrQGINQiqHRcfYNjyP9oKM72r/Zae/6hbG3dDyVZAJEUqdhc32FlaU5olYTpRQgEcK5AqlsL4eO3kS9WubC2dNInOl/Pgskr3pDgI4jevoGmT58lKXFCywvzOD7AqTFSkNsYlLZHNNHb2Fk/0GsSqG1vsLgLt24X2vZvawTYViLQdI7OMrBG28jX+gnNhqEW7FKBTTrFc6cepJsvpuJg0fc5F3D8lxRIG0fI5PvZvqGYyxfXGRlYY6UrzqDi2JNV+8gh4/dQld3L1obd+eSWX6xccZVixBI3JJPBRkOHLmJ/uH9xMaAcNd9pYgaNWZOnSBf6Gd08hBxbJ63T/LSfwUCg0b6AdM33MxWaYPluRlSnpcoT0UcW/oHRzl05DjKzzgHDRLX8l+y7HKqhGR84hAjY5PE2oJwvowvfVq1MhfOnqR/eIy+faPEUYQQXNEkX7ZCrABtYOrADZhYc2HmNJ5srwtBFEf0DQ4xdfAwCIExOqncviBnWbTjlxe0ki4JKaxlaHSSkdGpxD9xvZK+T3VrneWFGcYPHCLbVcBqjbzU4nCJQITQaB0zMDROT6HA7NlTYDRCOhc6jA3d/UNMHjyCxVmRdp9e+KBewpJ4xUNjkwyOThBq24EKPM9jfXmJ7XKZ8YOHsVIh7OXbZ49ArLEEQRdjExPML8zSrJWRSjicwhiyXXkmpw9jhYdJorMrCPlfpewYMomxMDI+RW//IHGsk7sWJWBx5gxBKsXg6ASRsbuedjXI3TVqA6OTB2g2GxRXllDK67jUUnlMHDiC72ewxu2+FyqMf66V1B6WEM5Mj08cJsh1YU3s9IWCKGywtDDP0OgoqWwOazQSmcA5TlE7t1wburoL9Pb2sjQ/B8YtJ4FAGxgen6Cru5BEuC+u4y8VdnG1IpI2lJ9ibOIAViTW0Qo8X1DauEir3nC6xtgkend92oXfGfaNjrO1tcV2uYSnlAN9tCXf08fg8BixNi483934VXTHv7ZOEcI5p13dffQPDqO1RSWQgrCa1cU5enr7SXfl0UQdUy0FAqMjst0FuroLLC8vIqVz5py3LBkem0QK56YLAVZYpE2WphUYDJHFSRsLxG6ZWs2OW7jbJIuO1bLWYI3BGhfW04ZMcNCisWAwWLS7Zxx41IYBrNWdz05bSe3JfAyNTBAEAcYaLOApj+2tTZq1bYZGJjDtfgvn+mOwDAyPUqvVqFfLKOkUZmwMhd4+8oWCc7wSLFTEMbG1tAiJTBNPKgIl8D3lBi5TGOVjpYfWMTZuEZsYYzTGxBgdo22MNrHDRqRESAFCEusYG4cYax3AJCxosEZisAgpnGtuTYK5qM4n0gZjY7C6I3prLV4qoH9oGG06ssJiWV9doqfQTzqdw1iDEOAZo1FBlp5CHwuzM0jrUDBrLEJK+vaNJULXaGOcJK0mEhI/FvgZn5mtKvdf2KY3LXjzDcPIraegdoa4+wb8/C2YCKSp7tLCAqElUsJWpUJkQAlJNpsm7XuAQWtLLYqptVoM9XSj4ybSkxS3I3wM+ZzP1nadyAiElPRkUvjJs7EBlTht7W1bGBxmY30VEzWwUqI8yXa5SBw16ekfZHXpAr4CzxhDb28/sTFsb22iEsDGGEO+0EdXT8HhG52QE6z18GWEn8nxaw+e58P3XmCzISCCv/meLb6z+k6q1VMEXh/hvu8guPGDWAK3lVAIq7HSYFWGH3z/7/DlR88RSEgFittfcSMffv8PcHh8iL/41Bf5wC/9EZ/4yAf41td+HQDf+74PMTU6xB9+8Mf4wf/8W9z7+GlSviTje7z+zmN88P0/zMSAU/7K83ZWiRfQU+inuDLvxigcGFXZLNLTN8DaxXnnxAkkfb2D1Mpl4qiFEMq5qxb6+gaRQnb0iROJwCiBl/L508eW+Jm/n2VbBXTnQZDiwtoy2HXs/h9FH3wvLH+K1rkPYz0ftEGgMUIlYQDMr2xz/NgUf/Y/f5JffN/beeTxZ/jOd/5XtDFEWlMs1XjXf/ldZi+uA1DcrFOuhQDMrVV4+c1H+PPf/El+6t1v5fP/+Djf/a5fpRlqhHT6xqkGp796+waQnucAbNx229raIEhlybRNsBekyWSzlDeLHSVkjMEPAroKfQ7YEYkSw4E8vq947+fm+OHPniUzkCUQFq9QwNqIjFUgMohYEafHEF03IhY+ga2ewQY5DAJpVCeO0Cbm6OQQb371rbzzu9/IZz76Czzz7Cz/dOIs2SCgZ3QfNp3hB97/WwD4gY+UiYI2ETcdGOJbXnUr7/2eb+Ezf/SLPPLkae57/Fmk9DCmrcjdpKZzeTLZbpf+AJRUNGt1wqhJvrsXbSwy15XHWqhVt50yxcF2uXweL8hgzC5g31r8lM/jF8v8/kOLBCmBl/fQCprrZTAOfCZs4s3/Kd5zH8UOvArrFbD3fxNm7XPgpYE6omPxBY1WSBjGtMIG02NDeIUe5lZKWANBKsVf/Ob7eOChU3zoY39LJpdBJ0rTYKg2Q8IophWGHJ0aIdvbw8zCIjtTSLLiHUDU1d2DTQQlEJg4plqrkMv3IJDIXHcPrbCFDhsgVKI0LV35HqRwsa+rM0kfCkWlGYMJUTVNfa1GKp1Gb1WhUceoADPxo5A6QGr5XkSUwbvjM9hmBXPujxA2wki1C7rTZLJZUimPIJXh1MwCcWmL6fFBEFCr13ndbUf5nV/5MX7uN/6MJ0+cp6fLYbNSQi4XkPI9glSKZ8/NU9+sc3hqvxtwx3XtGB2y+W5QHsIY1wVhaVbKpDI5lJ/Cy+a6aNRrLohLIEEpPTK5PG2H0ra9POnRiFr8xpfOQ8NiCzG5Qi/xehlLDDGoRgPh9yFy07Rqi5DyEU9+CE94EJYBg7AKK2JAIa3hqadm+LO/+TKLG1t8+A8/xW133Mwrjh/k/keeITSazWqN93zPm3ngsSf55B/fjX3TK9sd45+eOscnPv1FltbLfPgjn+XOV93Ia192BKPjPXnjtrUJMjl8P40JG05WUtCq11BKEQRpvFQ6w1ZxzUWFzl1DptL46Sy78QZjLUGQ4i8fOcPnn1whyAbIGKLlDaJShdz4IGFpDSu6YPVRootP4R3+Iez5T+JvPoLIZPgD8zKGyhHf2ROgoxBIcezoFA8/dZpf/uj/RWjF9/7bb+DnfvytSAT57i5ecWQUD4U1lt/+2R9j9uwy+3pyaK25+cZJHnniLB/6/c8SYfn+7/gGfuE9343y02CiK2J0npciSGWot+od8LkVhhhjCIIA0WzW7fzZk2xvbSC9AKtj0vkCh4/dtieJFGpNJhXwQx9/kE98ZYbMQBemATZskhrqQfiWyjNr/M5b+/hx+x6at/48ZvVeZHme0oG3c29F86PeHbwp38v/ueGgW00yQqg04BwtJdo5lxgdRyg/41rXIQaBUpekMawlNhqpBBK1c9mEOGxVJsDy3rI0e5bN9SWUr5zFsTB948uobm3gYa3DQYVECIOxBj9JIO1OGUjrGhRRCK0W0qRRQ3lMFGBrTczGOkQgdIzMpMmuPArL99A8+MPcN/Yevpy6SP3iBS6YOg1j6MKC8Lj3/oe46YZDDA70Y+IYbVx44PkpHnz4EcbHRxkfHUUKyYWFRb5034MYa8hms7zlja+npytLs9ni03d9geXVDW4+fozX3PlKAm8PNJ3Iz60IL0glrkTb5wrRUYhMBUhjTAKp7Tzq+V4nYgQwtOF7zWtuGMI2KtiVIvbUHHpxhXirjAwNMqrTAE54N3DfhUf5tP8KfqJ8hE/NnODhlUUILQNCkxOKljAI6fHxv/prLiwsgZDO7EkH5pQqDd73M7/Ixz7+V0jpUP5Hn/gqn/77u9Bhi/vvf4Cf+2//HYvkw//jf/HYV5+mkO/i7i/cTbVaTfypK0fVnuclGrftaCauhvLwrLUubmij/Ljg59IY3xOGsBXyfXce4a6HzvDpR2cJfIlqxoi+PDbTDcUi62aA78j9Aotei1in0c0KrG4AhgmV4lcPH0AIkInpy+dyeH6y+hJIUnmKz/79XbzlW97ARrHE3MI8k/sn0Nrwmju+nne94wc5cfoMv/W7f4C1lpOnTvG2t72Vt337tyaDiLBWuy1zhaKUuky/6Dh2Po7bQzqx1a4CR0TZlbzBYoUg0hB4Hm/5umlstUw2342OIsLZOUyzifE90DEmDsGG9ARN+gKPIU+htiNu78ryyt4+4ihGJZ3VJkKbhDgTx0jlEccx9z3wIO9+549w7Mhh7rrnS1gLQTrg83ffy/ve/7P8xE//PK++43aklLzv3e/ibz71Wb7r+9/B7/3xx9FG7PGud8bhyk4+mSS+ciAYVl49L3NFyQqBMTFfd2iAnIgob2yTymfBGvwwRjSaaBshw4hofZvmZpU4lGwVG+hymZfnsm557oICpPDo7u5BSomfyaKUz4lnTzJzYY4//OM/4amnn+G+Bx5CCIjDOm98w+v47V//FT75v3+f+x54iOWVVV51x+188k/+gN/79V/lc/f8Aw898ljiqX6NQJQATwiBlAK966rW5oqomJSCsNXi1v1DfOw/fRc/9ZFPs3C2Sro7j6huQX2TKGxh6hI/lkgEtY0iXVHEv79hknffcAgbh0gpOvBIrd7i81/4MheOzBPGId/0mtfy8b/8a77v7W/j2970BoyxvPenP8DDjz5BJpvj1HPPcf/Dj3B+bp5qfRupFL/8K7/G5MFDTE6Mkg7S9BZ6cC7D3v63lWw7mdYByAGpnBHxhBRI6RHTcmiSsGjd6kCIl+Y+lVKErZC3v+E23nT7EX7mI3/HR//2KzR1GUyD1xyZ4KvFErPFIq3tNN841MvvfftrOd7bjdUaYw2elRic0n7LG7+R06dO8/iT23hK8PJbbuO2W2/l333bm+jt7gHgx3/kHVS3qxw7eiNHpk/w4MOPEBv4pQ/8FPsGB3jDG76Jz93zJU6ceIr/+B/ewfFjN2J0hFRXTl3rWLtx2XbuWCCVh45jRLNVtxeee4ZaZRPl+eg4oqvQx6Gjt2HZxS40OsnBCIy1mDgmHaSxSnLvY8/x5KlZbjo8zpvvuInz5Rp3n71AbzbNvzkyRUFKwtggZZsPBOAyfZ6fZrdxtEYjpAITJTNpd/yRK3DhjI4vG7jVoXMjZDvTyJ7nVxZnWL84n9AzDLGG6aO30GzU8LDge36HuiSEIApdZ6TyLsdFrSUIMhC4Pe15Gb75lcf45lce66zLQz0Bh155s+uMjkB5eEojrLykPjfgtlI31iTOl3HbNsmd2LiJ8NIIAVrHyRJ3g5Wq7UtoJI521U7WX1rabbfCZgIJODhSKYmf8qmUW3hRHJHJZCjt4mREUUQUhaQ93+GctKNgi/J97r//AbQ23HHn7Tzx+FNM7N/P5+/+Aq9/3evZKBU5Mn2AIC1QQlJvNXn21JNM7Z/GxCGx0VSrNRCCrnyes2fPcmBqyiFmuSwbG0VW14u8+s7bERiE8qk1GvzD5+7i+PHjZDNpUqmA+YV5rIWJyUnmFxYYHR4mDJuMDg/jKbUHRtwzn8YQNpsJ98S5qUp5SKloNuvIVr1OKpPvkFmEkNhYEzZqiQ5p1+QgPxNrSptlilsV/vH+h/nLv/okpeIGfT09RGGLj//pn/Pc2TM0myEnnjmJJxVfvvdBPnvX51lZWWVpaZm7vnAPn/m7u7i4sspXHnyYp048y8lTp3n66WfY2ipz4umnqNWrLF5cZn5hgWq1TrXRYGZunnPnZzh95iyzs3OMjuxjYWGBj/3JJ7BYTp48zep68TIfaneJwxZxqwVSYa3EGk2QyYKQRI0aYn7mlO3rH+bMs48lDEBJHGuGxycZnTzslqgQjpVsWnhewMOPPI7yfQYHBqhWt+nqypFOp4nCkK1KlXTa49D0NFoboiikWCpT2a7S39uNMYB0q9BP+Tz99NPcfPwmSqUS1WqV48eP8+ijj3LH7V9POh2AhTCK+cf7vsLxm46T8n1SqRSLCwvEccTk1AFW1tbpyefY3CpT2tzkda++E2vMnlimrT8qpXXmZk6ilGM+6bjF4NgBevsGOffsE4hTX33ITh25lfOnn6DVaKCEhzYx2e4Ch469bEclGdCmiUDhB+mOvrga7cOYCGsMyktd/UfXLI61+DVnxkyUkGouF8ji3Fk21xfxlIe1Eq0jpo7eimm1mJ85ideo1Yl1SL67n2ZtHjyLlIJGrUqzViWbd5CbAwecrQ4b9aQR8FI+Z8+fY211jVtuvRXf99ja3KK3t0A6nebiyiozs3P0dOeZGBsh19VFvVZno7RBV1eegf4+rIViscSZs2d5+a23gZRIJamUt0gHaYIgQCqHwbap4Fpr0ukMG+tF6o0akxOTjqmY+FUdI8GObjQ6or5dTnBiAVbj+wGZbBcr68sIBF4cR9S2y/T09rO2PJ88LNFxRHlznVziCzhmjkgE3g58LMpTlKsNVJDhc3f/A1EY0tffRxTFTE1OUK9VGR0bZ3VtnQceeYxisciBqSlWN9bJZjJ4yuMb7ridteIGpXKZZ06dZm19g2qrST6TRQlBrGPq9QZgMcYyPLyPjWKRIEjRakVMTk4wNSXBOMCnTQfrcNSs+3+7skXYqKOUw1i10eQL/QgB1e0KQko8KQTl0jp9h44TZLLEzSZCKaR01wdHxpGeD6iOiWsXawzWCnK5HOVymSOHD1PaLLF//34W5hfIpgP2jw5z5tx5Cr19tOp1UsMjTE9PMzA0iNaa0ydPUSqVGBwYYKtcYWRkmIGBQe66+wuM3nQzY6PDSClZXV0jk8nQaDSYmNhP30YfYNnerjG8b5+bM7kTxe5ldLl/ttbXwBoQ7Whe0NM/SKNaIWw5RqV44oEvWivg6M23s7mxzPL8LF7Kdy5urNl/6EYGhsd2WEJ72nGOmyO77REVbQrC8+mPMAppNRpkc12X1TE3P09/Xz9dXbmrPr+nxT1O224vxAKSRq3CzOmnHUYsnXXx/AxHbnoZi7Pn2Cqu4XnSxTJxHFJcX2FwaIT15SWw2tEcpaC4ukRv/6CT/hUojbArNthV2nz1vTndzl2EgJSfIuWndlfYWe6TExN72njecllifbd36lKfGyuLGBOhlI+0EMaawZEh4lhT2SqhPLfVpMXiSY/N9RWkUhQGhtCx8yClFNSqZTbWLiZm6mr9EVf5XO3ejte4Z8C7Bmat7cz6NT9XkZNNcJ7q9hZbm0XHdwGMsXh+hv6hYYrrK2gddYQoXfpOEbUarK+vMTw6jlSOOG8BJSyrF+dp1GsJteql5XY831mcl4JOYYxhZXEBYXYy3UYb+odGAEVpbQVPSmySFpEioTMIKdi4eAGpFP3D486EIRDSJ261WJmfcVohyeLtLlda1u0Zvlq51v0XVxxVQghBcWWBeqXkYh8rwMSoIMvg6Djry3PoqOliJgC7kz5DSkkUtlheWmBsfD+pINdhJCul2CytsL4yjy+9jjT/fy3OzEpq2yXWluecmU1kHxkY2b+fOGxRXF1BXXIaS+5UYvE8xcbaEo1Gg/1Thzo5UAApJBfnzlPZXMfzXrojXf8cK0UIQdiqs3j+OZfwxvFK4zikuzBAoX+Qi3PnMVonaQjb+VwGIQpjmZ+ZoVDoZXB4lFjrZC9LsJYL509T3y6jPKdnBG0g6epb51+m2A7KruOIuXOnCFstpEhOcRqD76eZmD7Ixtoq5a0SyrscQb3E07JIKWlUy8zPzTJ+4DC5rh6MjhDCEWh02GL2zLM0a9soz8N0BPGvy8+0zl6j45C5cydpVrcd9SEh+FgDEwePEkUxFxcuJAzLy/u8l6eaeP7KE6ytLFLa2ODQjcfx/IwjzQBKeYStBudPP0WtUkJ5/h7z+MIH9MIF2m4/DJtcOPsMtXLJoWiJ2Y11zOjkNJl8NxfOnUaYGCHYk1lol70C6VgQiy8NCzNnqDVDpo/dglBeQnKzCE8RhS1mTp9gc23FJX7YCaj+ZVZLm0zuhFGvVjj/3Amq21sJc8gJI4piBkcn6R8eZ+7saaJ6Qvu4ygTspXYnY3EMGwXWMPvc02AtB4/dipCeg+gsSKkwWjN3/hSLs2cxJkRIxyJ25wclu5G261kB1/W7NrXL2g5BdGN1kdnnThA36njSd5RzaYnikIHRcUb3H2Rh5jTb5fVkRV+9+qvmZSwWqcDoJmdPP42SHkeO3YrnZTCxThjDEiktqyuznDn5FNubG3hCIZXCCIO9otv+wou1FpMklhCSZq3G7JlTLM6dw9od+oOwoCPD8NhBxiYOszj7HKXiRTxPXNM3ep4zd4lOEMadQVYe00dvIpXOMHPqBPVqGd/3XaxAglNIQW/fAIMjY2S7CojkmFmbsbObr3HFFjuoQjtiFXvim3ZpNesUV5bYXF9F6xjpqURfuGP0CMHY1CF6B/axcP45NjdW8f02BnJ1PXfNc7siOaPmCLYxVvrsnz5Mf/8gc7PnKa4uoSSO1JtwP7WOkVJRKPTTOzRErrsXzwtcg9iOenm+ZesQ8b0IvbUxjWqFrY11tkpFosjRNIVIDkFaQ6xj0tluJqYP4QcZZs+dolEpomSSVei42lc/2n/9x1RxJyu1FQyOjrF/YoqtUomlCzNErRqe53U0t7XWOXVCks7m6O7upaunkFCnApAe14QVrSaKWrSaDaqVCtXyJo3atks3yJ1jseDywxaP/qERRicOUKtVmZ95jrjZwlMqyRxcfWx7rl/rdRmdg4S7RBPrmGy+m8npI6SCDMuLcxTXlrFJtqxTnwWsSc7VCFQqRZBKE6Qz+Cn32gzlech28ksbojhChy2arQatsIFuhVhjkDI53b0L87DaoK0l293NyP5pcrk8K0tzrC0vIYVBCkWbBn695boFsiMUixQu/2ukZHBkjJGxKaKwxcrFi5SLK5g4QkqZvO9DYhKTbG2cvOCADnYkXAJkD8Jlafs1Cinc0Y0k+sIamzCqId3Vw76RMXp6B9iubLE8P0OzXnV5GZL3C+xEpNcnkBf0MgR3MUHVYvx0ln2j4/QN7iOOQkrra2yWNggbNcB5uDI5iX3lru0AwUnlO1cTU2yscVk2P6Cru8DA0D5y3QUa1W1WL86zXd5Ewot+dcZ1CWRvZ/dea+d9Y2MIgjS9Q2P0Dw7heR61WpXyVpFaeZOw1cDECUU8sV5yZ+ohEZZlty8iERJ8P0Uu10137wC5QgElFZXKFpuri1QrZRyY9dK8G+ZFCyQZi7MyxqBjl4vJ9xQo9A/Qle9GeT5xHNNq1GjUGzSbTXTUIo6ihG2843F6vo/0fIIgSzbbRZDJEKQDLIZmvU5ls0S5VKLVrCGkYyOQJNKwXGKZLl151zHO63mhynULhjbwbDrvHlKeTyabJdeVJ5PvIQjS+F6AVKKTlG77G23hGm3QWtNqhYT1berVMrV6jSgMOwFoJ/diL+/Diykv3TuIkuJmRbiXMCXCqW9XqFXKWLGEkAolFZ6fcqtBio5itdZitCaKQrTWbvVY7d4eI5ySbiP9/1yowv8Dp12/nRLdr5MAAAAASUVORK5CYII="""


A4_WIDTH  = int(595 * 0.75)
A4_HEIGHT = int(842 * 0.75)


def verarbeite_pdfs(dateien: list, ausgabe_ordner: Path, ausnahmen: list, log_callback):
    if not dateien:
        log_callback("❌ Keine PDFs ausgewählt!\n")
        return

    ausgabe_ordner.mkdir(exist_ok=True)
    log_callback(f"✅ {len(dateien)} PDF(s) wird verarbeitet...\n")

    for pfad in dateien:
        pfad = Path(pfad)
        ausnahme = pfad.name in ausnahmen
        log_callback(f"⏳ {pfad.name}...")

        try:
            ausgabe = ausgabe_ordner / pfad.name
            doc = fitz.open(str(pfad))

            gedreht = 0
            for nr in range(len(doc)):
                seite = doc[nr]
                if not ausnahme and seite.rotation != 0:
                    # Rotation direkt auf 0° zurücksetzen (90, 180, 270 → 0)
                    seite.set_rotation(0)
                    gedreht += 1

            info = f"{gedreht} Seite(n) auf 0° korrigiert" if gedreht > 0 else "keine Rotation nötig"
            if ausnahme:
                info = "übersprungen (Ausnahme)"

            doc.save(str(ausgabe), garbage=4, deflate=True, deflate_images=True,
                     deflate_fonts=True, clean=True)
            doc.close()

            vorher = pfad.stat().st_size
            nachher = ausgabe.stat().st_size
            ersparnis = (1 - nachher / vorher) * 100
            log_callback(f" ✅ {info} | {nachher/1_048_576:.1f} MB ({ersparnis:.0f}% kleiner)\n")
        except Exception as e:
            log_callback(f" ❌ Fehler: {e}\n")

    log_callback(f"\n📁 Fertig! Dateien in: {ausgabe_ordner}\n")


def fuehre_zusammen(dateien: list, ordner: Path, ausgabename: str, log_callback):
    if not dateien:
        log_callback("❌ Keine PDFs ausgewählt!\n")
        return

    log_callback(f"Füge {len(dateien)} PDFs zusammen...\n")
    neues_doc = fitz.open()

    for pfad in dateien:
        pfad = Path(pfad)
        if not pfad.exists():
            log_callback(f"   ❌ Nicht gefunden: {pfad.name}\n")
            continue
        doc = fitz.open(str(pfad))
        neues_doc.insert_pdf(doc)
        doc.close()
        log_callback(f"   ✅ {pfad.name}\n")

    ausgabe = ordner / ausgabename
    neues_doc.save(str(ausgabe), garbage=4, deflate=True, clean=True)
    neues_doc.close()
    log_callback(f"\n📄 Gespeichert als: {ausgabe.name}  ({ausgabe.stat().st_size/1_048_576:.1f} MB)\n")


class DateiListe(tk.Frame):
    """Wiederverwendbare Dateiliste mit Checkboxen und Drag-Reihenfolge"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#F5F7FA", **kwargs)
        self.vars = {}   # filename -> BooleanVar
        self.order = []  # Reihenfolge der Dateien
        self._build()

    def _build(self):
        # Header
        header = tk.Frame(self, bg="#F5F7FA")
        header.pack(fill="x")
        tk.Button(header, text="☑ Alle", font=("Segoe UI", 9),
                  bg="#e5e7eb", relief="flat", padx=8, pady=3,
                  command=self.alle_auswaehlen).pack(side="left", padx=(0,4))
        tk.Button(header, text="☐ Keine", font=("Segoe UI", 9),
                  bg="#e5e7eb", relief="flat", padx=8, pady=3,
                  command=self.keine_auswaehlen).pack(side="left")

        # Scrollbare Liste
        container = tk.Frame(self, bg="#F5F7FA")
        container.pack(fill="both", expand=True, pady=(6,0))

        self.canvas = tk.Canvas(container, bg="white", highlightthickness=1,
                                highlightbackground="#d1d5db")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.liste_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.liste_frame, anchor="nw")
        self.liste_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self.canvas.itemconfig(self.canvas_window, width=e.width)

    def lade_dateien(self, dateien: list):
        """Lädt eine Liste von PDF-Dateipfaden direkt"""
        for widget in self.liste_frame.winfo_children():
            widget.destroy()
        self.vars.clear()
        self.order.clear()

        if not dateien:
            tk.Label(self.liste_frame, text="Keine PDFs ausgewählt",
                     font=("Segoe UI", 10), bg="white", fg="#9ca3af").pack(pady=20)
            return

        for i, pfad in enumerate(dateien):
            pfad = Path(pfad)
            var = tk.BooleanVar(value=True)
            self.vars[str(pfad)] = var
            self.order.append(str(pfad))
            zeile = tk.Frame(self.liste_frame, bg="white" if i % 2 == 0 else "#f9fafb")
            zeile.pack(fill="x")
            cb = tk.Checkbutton(zeile, variable=var, bg=zeile["bg"], activebackground=zeile["bg"])
            cb.pack(side="left", padx=(8, 0))
            groesse = pfad.stat().st_size / 1_048_576
            tk.Label(zeile, text=pfad.name, font=("Segoe UI", 10),
                     bg=zeile["bg"], anchor="w").pack(side="left", fill="x", expand=True, padx=(4,0), pady=6)
            tk.Label(zeile, text=f"{groesse:.1f} MB", font=("Segoe UI", 9),
                     bg=zeile["bg"], fg="#6b7280").pack(side="right", padx=12)

    def lade_ordner(self, ordner: Path):
        """Lädt alle PDFs aus einem Ordner"""
        for widget in self.liste_frame.winfo_children():
            widget.destroy()
        self.vars.clear()
        self.order.clear()

        pdfs = sorted(ordner.glob("*.pdf"))
        if not pdfs:
            tk.Label(self.liste_frame, text="Keine PDFs gefunden",
                     font=("Segoe UI", 10), bg="white", fg="#9ca3af").pack(pady=20)
            return

        for i, pdf in enumerate(pdfs):
            var = tk.BooleanVar(value=True)
            self.vars[str(pdf)] = var
            self.order.append(str(pdf))

            zeile = tk.Frame(self.liste_frame, bg="white" if i % 2 == 0 else "#f9fafb")
            zeile.pack(fill="x")

            cb = tk.Checkbutton(zeile, variable=var, bg=zeile["bg"],
                                activebackground=zeile["bg"])
            cb.pack(side="left", padx=(8, 0))

            groesse = pdf.stat().st_size / 1_048_576
            tk.Label(zeile, text=pdf.name, font=("Segoe UI", 10),
                     bg=zeile["bg"], anchor="w").pack(side="left", fill="x",
                     expand=True, padx=(4,0), pady=6)
            tk.Label(zeile, text=f"{groesse:.1f} MB", font=("Segoe UI", 9),
                     bg=zeile["bg"], fg="#6b7280").pack(side="right", padx=12)

    def alle_auswaehlen(self):
        for var in self.vars.values():
            var.set(True)

    def keine_auswaehlen(self):
        for var in self.vars.values():
            var.set(False)

    def get_ausgewaehlt(self):
        """Gibt die ausgewählten Dateipfade zurück"""
        return [p for p in self.order if self.vars.get(p, tk.BooleanVar()).get()]

    def get_ordner(self):
        if self.order:
            return Path(self.order[0]).parent
        return None


class PDFToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Tool – DND Labs")
        self.geometry("750x680")
        self.resizable(True, True)
        self.configure(bg="#F5F7FA")

        self.blau   = "#1E3A5F"  # DND Labs Dunkelblau
        self.akzent = "#2563EB"
        self.hell   = "#EFF6FF"
        self.gruen  = "#16A34A"
        self.grau   = "#6B7280"

        self._build_ui()

    def _build_ui(self):
        # Header mit DND Labs Branding
        header = tk.Frame(self, bg=self.blau, pady=14)
        header.pack(fill="x")
        inner = tk.Frame(header, bg=self.blau)
        inner.pack()
        try:
            data = base64.b64decode(LOGO_B64)
            self._logo = tk.PhotoImage(data=data)
            w = self._logo.width()
            if w > 100:
                f = max(1, w // 80)
                self._logo = self._logo.subsample(f, f)
            tk.Label(inner, image=self._logo, bg=self.blau).pack(side="left", padx=(0, 14))
        except Exception:
            pass
        tf = tk.Frame(inner, bg=self.blau)
        tf.pack(side="left")
        tk.Label(tf, text="PDF Tool", font=("Segoe UI", 22, "bold"),
                 bg=self.blau, fg="white").pack(anchor="w")
        tk.Label(tf, text="Drehen · Komprimieren · Zusammenführen",
                 font=("Segoe UI", 10), bg=self.blau, fg="#93C5FD").pack(anchor="w")

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[12, 6])
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=(0, 4))

        # Footer mit Copyright und klickbarem Link
        import webbrowser
        footer = tk.Frame(self, bg="#E2E8F0", pady=5)
        footer.pack(fill="x", side="bottom")
        footer_inner = tk.Frame(footer, bg="#E2E8F0")
        footer_inner.pack()
        tk.Label(footer_inner, text="© 2025 DND Labs  |  ",
                 font=("Segoe UI", 8), bg="#E2E8F0", fg="#6B7280").pack(side="left")
        link = tk.Label(footer_inner, text="dndlabs.de",
                        font=("Segoe UI", 8, "underline"), bg="#E2E8F0", fg="#2563EB", cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: webbrowser.open("https://www.dndlabs.de"))
        tk.Label(footer_inner, text="  |  Alle Rechte vorbehalten",
                 font=("Segoe UI", 8), bg="#E2E8F0", fg="#6B7280").pack(side="left")

        self._tab_drehen(nb)
        self._tab_zusammen(nb)

    def _tab_drehen(self, nb):
        frame = tk.Frame(nb, bg="#F5F7FA")
        nb.add(frame, text="  🔄  Drehen & Komprimieren  ")

        # Ordner oder Dateien wählen
        tk.Label(frame, text="PDFs auswählen:", font=("Segoe UI", 10, "bold"),
                 bg="#F5F7FA").pack(anchor="w", padx=20, pady=(16, 2))
        ordner_frame = tk.Frame(frame, bg="#F5F7FA")
        ordner_frame.pack(fill="x", padx=20)
        self.dreh_ordner = tk.StringVar()
        tk.Entry(ordner_frame, textvariable=self.dreh_ordner, font=("Segoe UI", 10),
                 width=40).pack(side="left", fill="x", expand=True)
        tk.Button(ordner_frame, text="📁 Ordner", command=self._waehle_dreh_ordner,
                  bg="#2563EB", fg="white", font=("Segoe UI", 9), relief="flat",
                  padx=8).pack(side="left", padx=(6, 0))
        tk.Button(ordner_frame, text="📄 Dateien", command=self._waehle_dreh_dateien,
                  bg="#475569", fg="white", font=("Segoe UI", 9), relief="flat",
                  padx=8).pack(side="left", padx=(4, 0))

        # Dateiliste
        tk.Label(frame, text="PDFs im Ordner – Auswahl per Checkbox:",
                 font=("Segoe UI", 10, "bold"), bg="#F5F7FA").pack(anchor="w", padx=20, pady=(14, 2))
        self.dreh_liste = DateiListe(frame, height=160)
        self.dreh_liste.pack(fill="x", padx=20, ipady=0)

        # Ausnahmen
        tk.Label(frame, text="Nicht drehen (Dateinamen, eine pro Zeile):",
                 font=("Segoe UI", 10, "bold"), bg="#F5F7FA").pack(anchor="w", padx=20, pady=(10, 2))
        self.ausnahmen_text = tk.Text(frame, height=3, font=("Segoe UI", 10),
                                      relief="solid", bd=1)
        self.ausnahmen_text.pack(fill="x", padx=20, pady=(0, 0))

        tk.Button(frame, text="▶  Starten", command=self._starte_drehen,
                  bg=self.gruen, fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=10)

        self.dreh_log = self._log_widget(frame)

    def _tab_zusammen(self, nb):
        frame = tk.Frame(nb, bg="#F5F7FA")
        nb.add(frame, text="  📎  Zusammenführen  ")

        # Ordner oder Dateien wählen
        tk.Label(frame, text="PDFs auswählen:", font=("Segoe UI", 10, "bold"),
                 bg="#F5F7FA").pack(anchor="w", padx=20, pady=(16, 2))
        ordner_frame = tk.Frame(frame, bg="#F5F7FA")
        ordner_frame.pack(fill="x", padx=20)
        self.zus_ordner = tk.StringVar()
        tk.Entry(ordner_frame, textvariable=self.zus_ordner, font=("Segoe UI", 10),
                 width=40).pack(side="left", fill="x", expand=True)
        tk.Button(ordner_frame, text="📁 Ordner", command=self._waehle_zus_ordner,
                  bg="#2563EB", fg="white", font=("Segoe UI", 9), relief="flat",
                  padx=8).pack(side="left", padx=(6, 0))
        tk.Button(ordner_frame, text="📄 Dateien", command=self._waehle_zus_dateien,
                  bg="#475569", fg="white", font=("Segoe UI", 9), relief="flat",
                  padx=8).pack(side="left", padx=(4, 0))

        # Dateiliste
        tk.Label(frame, text="PDFs im Ordner – Reihenfolge per Checkbox wählen:",
                 font=("Segoe UI", 10, "bold"), bg="#F5F7FA").pack(anchor="w", padx=20, pady=(14, 2))
        tk.Label(frame, text="Die Reihenfolge in der Liste bestimmt die Reihenfolge im Ergebnis",
                 font=("Segoe UI", 9), bg="#F5F7FA", fg=self.grau).pack(anchor="w", padx=20)
        self.zus_liste = DateiListe(frame, height=180)
        self.zus_liste.pack(fill="x", padx=20)

        tk.Label(frame, text="Name der fertigen Datei:",
                 font=("Segoe UI", 10, "bold"), bg="#F5F7FA").pack(anchor="w", padx=20, pady=(10, 2))
        self.ausgabename = tk.StringVar(value="Zusammengefuehrt.pdf")
        tk.Entry(frame, textvariable=self.ausgabename, font=("Segoe UI", 10),
                 width=40, relief="solid", bd=1).pack(anchor="w", padx=20)

        tk.Button(frame, text="▶  Zusammenführen", command=self._starte_zusammen,
                  bg=self.gruen, fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=10)

        self.zus_log = self._log_widget(frame)

    def _log_widget(self, parent):
        log = tk.Text(parent, height=6, font=("Consolas", 9), bg="#1e1e1e",
                      fg="#d4d4d4", relief="flat", state="disabled")
        log.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        return log

    def _log(self, widget, text):
        widget.config(state="normal")
        widget.insert("end", text)
        widget.see("end")
        widget.config(state="disabled")
        self.update_idletasks()

    def _waehle_dreh_ordner(self):
        d = filedialog.askdirectory()
        if d:
            self.dreh_ordner.set(d)
            self.dreh_liste.lade_ordner(Path(d))

    def _waehle_dreh_dateien(self):
        dateien = filedialog.askopenfilenames(
            title="PDFs auswählen",
            filetypes=[("PDF Dateien", "*.pdf"), ("Alle Dateien", "*.*")]
        )
        if dateien:
            self.dreh_ordner.set(str(Path(dateien[0]).parent))
            self.dreh_liste.lade_dateien(list(dateien))

    def _waehle_zus_ordner(self):
        d = filedialog.askdirectory()
        if d:
            self.zus_ordner.set(d)
            self.zus_liste.lade_ordner(Path(d))

    def _waehle_zus_dateien(self):
        dateien = filedialog.askopenfilenames(
            title="PDFs auswählen",
            filetypes=[("PDF Dateien", "*.pdf"), ("Alle Dateien", "*.*")]
        )
        if dateien:
            self.zus_ordner.set(str(Path(dateien[0]).parent))
            self.zus_liste.lade_dateien(list(dateien))

    def _starte_drehen(self):
        ausgewaehlt = self.dreh_liste.get_ausgewaehlt()
        if not ausgewaehlt:
            messagebox.showerror("Fehler", "Bitte mindestens eine PDF auswählen.")
            return
        ordner = Path(ausgewaehlt[0]).parent
        ausgabe = ordner / "komprimiert"
        ausnahmen = [z.strip() for z in self.ausnahmen_text.get("1.0", "end").splitlines() if z.strip()]
        self.dreh_log.config(state="normal"); self.dreh_log.delete("1.0", "end"); self.dreh_log.config(state="disabled")
        threading.Thread(target=verarbeite_pdfs,
                         args=(ausgewaehlt, ausgabe, ausnahmen, lambda t: self._log(self.dreh_log, t)),
                         daemon=True).start()

    def _starte_zusammen(self):
        ausgewaehlt = self.zus_liste.get_ausgewaehlt()
        if not ausgewaehlt:
            messagebox.showerror("Fehler", "Bitte mindestens eine PDF auswählen.")
            return
        ordner = Path(ausgewaehlt[0]).parent
        ausgabename = self.ausgabename.get().strip() or "Zusammengefuehrt.pdf"
        self.zus_log.config(state="normal"); self.zus_log.delete("1.0", "end"); self.zus_log.config(state="disabled")
        threading.Thread(target=fuehre_zusammen,
                         args=(ausgewaehlt, ordner, ausgabename, lambda t: self._log(self.zus_log, t)),
                         daemon=True).start()


if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()
