"""
Ce script réalise la migration de l'ancien logiciel vers le nouveau.
Un fichier json data.json doit être présent, au même niveauq que le script. Ce fichier doit conenir le données à migrer.
La fonction validate_data permet de vérifier que les données sont au bon format.
La fonction migrate permet de migrer les données.
La fonction reservations permet d'obtenir les liste des réservations sur les chambres, la migration directe ne pouvant être faite
"""
import json

from gestion.models import School, Rent, Renovation, Room, Leasing, Tenant

# todo : proprifier le code + réservation
def validate_data():
    with open('data.json') as f:
        data = json.load(f)
        leasings = data["dossier"]
        for leasing in leasings:
            bail = leasing["Caution"].split(".")
            if len(bail[0]) > 3:
                print("Issue with leasing, tenant : " + leasing["CodeLocataire"])
                print(leasing)

def reservations():
    with open('data.json') as f:
        data = json.load(f)
        rooms = data["chambre"]
        for room in rooms:
            if room["Reservation"]:
                print("Chambre " + room["Chambre"] + " - " + room["Reservation"])

def migrate():
    with open('data.json') as f:
        data = json.load(f)
        schools = data["ecoles"]
        rents = data["loyer"]
        tenants = data["locataire"]
        rooms = data["chambre"]
        leasings = data["dossier"]
        previous_leasings = data["historique"]
        renovations = []
        lht = {}
        for room in rooms:
            renovation = room["Renovation"]
            if renovation not in renovations:
                renovations.append(renovation)
        i = 0
        tot = len(renovations)
        for renovation in renovations:
            i += 1
            print(str(i) + "/" + str(tot) + " - Rénovations")
            new_renovation = Renovation(name=renovation, description="Niveau de rénovation " + renovation)
            new_renovation.save()
        i = 0
        tot = len(schools)
        for school in schools:
            i += 1
            print(str(i) + "/" + str(tot) + " - Écoles")
            new_school = School(name=school["Ecole"] or "École inconnue")
            new_school.save()
        i = 0
        tot = len(rents)
        for rent in rents:
            i += 1
            print(str(i) + "/" + str(tot) + " - Loyers")
            new_rent = Rent(pk=rent["CodeGenre"], type=rent["Genre"], rent=rent["Loyer"], service=rent["Supplement"], charges=rent["Charges"], application_fee=rent["FraisDossier"], surface=rent["Superficie"])
            new_rent.save()
        i = 0
        tot = len(tenants)
        for tenant in tenants:
            i += 1
            print(str(i) + "/" + str(tot) + " - Locataires")
            try:
                school = School.objects.get(name=tenant["Ecole_et_Annee"] or "École inconnue")
            except:
                school = School(name=tenant["Ecole_et_Annee"])
                school.save()
            new_tenant = Tenant(
                pk=int(tenant["CodeLocataire"]),
                name=tenant["Nom"],
                first_name=tenant["Prenom"],
                gender=tenant["Sexe"],
                school=school,
                date_of_entry=None if "0000" in tenant["DateEntreeRez"] else tenant["DateEntreeRez"],
                date_of_departure=None if "0000" in tenant["DateSortieRez"] else tenant["DateSortieRez"],
                observations=tenant["Observations"],
                temporary=bool(int(tenant["Passager"])),
                cellphone=tenant["Mobile"].replace(" ", "")[:10],
                leaving=bool(int(tenant["Va_partir"])),
                waterproof_undersheet=bool(int(tenant["alese"])),
                pillow=bool(int(tenant["oreiller"])),
                pillowcase=bool(int(tenant["taie"])),
                blanket=bool(int(tenant["couverture"])),
                sheet=bool(int(tenant["drap"])),
                birthday=None if "0000" in tenant["DateNaissance"] else tenant["DateNaissance"],
                birthcity=tenant["VilleNaissance"],
                birthdepartement=tenant["DeptNaissance"],
                birthcountry=tenant["PaysNaissance"],
                street_number=tenant["N"] or None,
                street=tenant["Rue"],
                zipcode=int(tenant["CP"]),
                city=tenant["Ville"],
                country=tenant["Pays"],
                email=tenant["Email"],
                phone=tenant["Fixe"].replace(" ", "")[:10],
            )
            new_tenant.save()
            lht[tenant["CodeLocataire"]] = tenant["Lot"]
        i = 0
        tot = len(rooms)
        for room in rooms:
            i += 1
            print(str(i) + "/" + str(tot) + " - Chambres")
            rent = Rent.objects.get(pk=room["CodeGenre"])
            renovation = Renovation.objects.get(pk=room["Renovation"])
            new_room = Room(lot=room["Lot"], room=room["Chambre"].replace(" ", ""), rent_type=rent, renovation=renovation, observations=room["Observations"])
            new_room.save()
        i = 0
        tot = len(leasings)
        for leasing in leasings:
            i += 1
            print(str(i) + "/" + str(tot) + " - Dossiers")
            try:
                tenant = Tenant.objects.get(pk=int(leasing["CodeLocataire"]))
            except:
                ignored_tenant += 1
                print("Can't find tenant. Ignoring")
                continue
            try:
                room = Room.objects.get(lot=lht[str(tenant.pk)])
            except:
                room = Room(lot=lht[str(tenant.pk)], room="??", rent_type=Rent.objects.get(pk=1))
                room.save()
            equiv = {
                "P": "direct_debit",
                "V": "bank_transfer",
                "C": "check",
                "E": "cash",
                "S": "special",
                "" : "special",
                " ": "special"
            }
            new_leasing = Leasing(
                tenant=tenant,
                room=room,
                bail=leasing["Caution"],
                apl=leasing["APL"],
                payment=equiv[leasing["Reglement"]],
                rib=bool(int(leasing["RIB"])),
                insuranceDeadline=leasing["EcheanceAssurance"],
                contract_signed=bool(int(leasing["ContratSigne"])),
                contract_date=leasing["DateContrat"],
                caution_rib=bool(int(leasing["CautionRIB"])),
                idgarant=bool(int(leasing["IdGarant"])),
                payinslip=bool(int(leasing["bulletinSalaire"])),
                tax_notice=bool(int(leasing["AvisImposition"])),
                stranger=bool(int(leasing["Etranger"])),
                caf=leasing["CAF"],
                residence_certificate=bool(int(leasing["CertifDom"])),
                check_guarantee=bool(int(leasing["ChequeGarantie"])),
                guarantee=False if leasing["Garantie"] == "0.00" else True,
                issue=bool(int(leasing["Probleme"])),
                missing_documents="" if not leasing["documentsnonfournis"] else leasing["documentsnonfournis"]
            )
            new_leasing.save()
            tenant.current_leasing = new_leasing
            tenant.save()
            room.current_leasing = new_leasing
            room.save()
        i = 0
        tot = len(previous_leasings)
        for previous_leasing in previous_leasings:
            i += 1
            print(str(i) + "/" + str(tot) + " - Anciens dossiers")
            try:
                tenant = Tenant.objects.get(pk=int(previous_leasing["CodeLocataire"]))
            except:
                ignored_tenant += 1
                print("Can't find tenant. Ignoring")
                continue
            try:
                room = Room.objects.get(lot=int(previous_leasing["CodeChambre"]))
            except:
                ignored_room += 1
                print("Can't find room. Ignoring")
                continue
            if tenant.current_leasing and tenant.current_leasing.room == room:
                leasing = tenant.current_leasing
                leasing.date_of_entry = previous_leasing["DateEntreeChambre"]
                leasing.date_of_departure = previous_leasing["DateSortieChambre"]
                leasing.save()
            else:
                new_leasing = Leasing(tenant=tenant, room=room, date_of_entry=previous_leasing["DateEntreeChambre"], date_of_departure=previous_leasing["DateSortieChambre"])
                new_leasing.save()
    print(str(ignored_tenant) + " opérations ont été ingorées car le locataire était introuvable")
    print(str(ignored_room) + " opérations ont été ingorées car la chambre étaoit introuvable")


#validate_data()
#migrate()
reservations()