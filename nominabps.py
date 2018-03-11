import csv


Funcionario = []
ArFunDiff = open('diferencias_SS_siap_bps.csv', 'w', newline='')
ArSiap = ('designaciones.csv')
ArBPS = ('nominabps.csv')


def CortarSSyCE(ss, ce):
    SeguroSalud = ss.split(" ")
    ComputoEspecial = ce.split(" ")
    SSCE = [SeguroSalud[0], ComputoEspecial[0]]
    '''
    devuelve tupla con:
    datos[0][0] = numero seguro de salud
    datos[1][0] = numero computo especial
    '''
    return SSCE


def NomSector(s):
    espacios = s.strip()
    sector = espacios.split("-")
    '''
    devuelve tupla con
    datos[1] = lugar o servicio
    '''
    return sector[1]


def BorrarEspacios(ci):
    ce = ci.replace("'", "")
    cedulabien = ce.strip()
    return cedulabien


def ArchivoDesignaciones(ad, ab):
    with open(ad, 'r') as siap:
        leersiap = csv.reader(siap)
        for cf in leersiap:
            ciAD = BorrarEspacios(cf[1])
            nfAD = cf[2]
            nfAD = nfAD[0:15]
            ssce = CortarSSyCE(cf[15], cf[16])
            ssAD = ssce[0]
            ceAD = ssce[1]
            secAD = NomSector(cf[13])
            alAD = cf[22]
            count = 0
            with open(ab, 'r') as bps:
                leerbps = csv.reader(bps)
                for cbps in leerbps:
                    cibps = cbps[4]
                    ssbps = cbps[20]
                    cebps = cbps[18]
                    if ciAD == cibps and alAD == "27":
                        if ceAD == cebps and ssAD == ssbps:
                            fila = [ciAD, nfAD, ceAD, ssAD, "", secAD, "ok"]
                            # print(fila[0], " -> ", nfAD, " ok")
                            count = count + 1
                        elif ceAD == cebps and ssAD != ssbps:
                            fila = [ciAD, nfAD, ceAD, ssAD, ssbps, secAD,
                                    "ERR: SS \n"]
                            print(fila[0], " -> ", nfAD, " Error SS")
                            count = count + 1
                            Funcionario.append(fila)
                        elif ceAD != cebps and ssAD == ssbps:
                            fila = [ciAD, nfAD, ceAD, ssAD, ssbps, secAD,
                                    "ERR: CE ver \n"]
                            print("ERR: ce ver")
                            count = count + 1
                            Funcionario.append(fila)
                    elif ciAD == cibps and alAD != 27:
                        count = count + 1
                        # print("nadaaaaa")
                if count == 0:
                    fila = [ciAD, nfAD, ceAD, ssAD, "----", secAD,
                            "ERR: no bps \n"]
                    print(fila[0], " -> ", nfAD, " - ", ssAD, " - ",
                          " -- ", ceAD, " -- ", " Error sin BPS")
                    Funcionario.append(fila)
        print(Funcionario)
        final = csv.writer(ArFunDiff)
        final.writerows(Funcionario)


ArchivoDesignaciones(ArSiap, ArBPS)
