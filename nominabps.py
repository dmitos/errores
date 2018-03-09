import csv


Funcionario = []
ArFunDiff = open('diferencias_SS_siap_bps.csv', 'w')
ArSiap = ('designaciones.csv')
ArBPS = ('nominabps.csv')


def CortarSSyCE(ss, ce):
    SeguroSalud = ss.split(" ")
    ComputoEspecial = ce.split(" ")
    SSCE = [SeguroSalud, ComputoEspecial]
    '''
    devuelve tupla con:
    datos[0][0] = numero seguro de salud
    datos[1][0] = numero computo especial
    '''
    return SSCE


def NomSector(s):
    sector = s.split("-")
    '''
    devuelve tupla con
    datos[1] = lugar o servicio
    '''
    return sector


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
            ssAD = ssce[0][0]
            ceAD = ssce[1][0]
            secAD = NomSector(cf[13])
            alAD = cf[22]
            count = 0
            with open(ab, 'r') as bps:
                leerbps = csv.reader(bps)
                for cbps in leerbps:
                    cibps = str(BorrarEspacios(cbps[4]))
                    ssbps = cbps[20]
                    cebps = cbps[18]
                    if ciAD == cibps and alAD == "27":
                        if ceAD == cebps and ssAD == ssbps:
                            fila = [ciAD, nfAD, ceAD, ssAD, "", secAD, "ok"]
                            # print(fila[0], " -> ", nfAD, " ok")
                            count = count + 1
                        elif ceAD == cebps and ssAD != ssbps:
                            fila = [ciAD, ";", nfAD, ";", ceAD, ";", ssAD,
                                    ";", ssbps, ";", secAD, ";", "ERR: SS"]
                            print(fila[0], " -> ", nfAD, " Error SS")
                            count = count + 1
                            Funcionario.append(ciAD, nfAD, ssAD, ssbps,
                                               'err ss')
                        elif ceAD != cebps and ssAD == ssbps:
                            fila = [ciAD, ";", nfAD, ";", ceAD, ";", ssAD,
                                    ";", ssbps, ";", secAD, ";", "ERR: CE ver"]
                            print("ERR: ce ver")
                            count = count + 1
                            Funcionario.append(ciAD, nfAD, ssAD, ssbps,
                                               'err CE ver')
                    elif ciAD == cibps and alAD != 27:
                        count = count + 1
                        # print("nadaaaaa")
                if count == 0:
                    fila = [ciAD, ";", nfAD, ";", ceAD, ";", ssAD,
                            ";", ssbps, ";", secAD, ";", "ERR: no bps"]
                    print(fila[0], " -> ", nfAD, " - ", ssAD, " - ", ssbps,
                          " -- ", ceAD, " -- ", cebps, " Error sin BPS")
                    Funcionario.append(ciAD, nfAD, ssAD, ssbps,
                                       'err BPS')
        print("termino")
        ArFunDiff.write(Funcionario)


ArchivoDesignaciones(ArSiap, ArBPS)
