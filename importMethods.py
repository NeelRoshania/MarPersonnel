import csv
import traceback
import setupDjango
from sales.models import CustomerID, DeliveryPlan
from production.models import RMReference
from quality.models import RDProject, ProductType, PaintInfo, ProductType
from django.contrib.auth.models import User
from datetime import datetime
import sys

def importCustomers():
    # Import customers
    try:
        with open('home/Resources/customerList17.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                accNo = row['Acc no']
                cName = row['Acc name']
                pName = 'N/A'
                pWorkN = 'N/A'
                pWorkE = 'N/A'
                newCustomerID = CustomerID(customerCode=accNo,customerName=cName,procurementName=pName,procurementWorkNum=pWorkN,procurementWorkEmail=pWorkE)
                newCustomerID.save()
                print(cName)
            print("\nSuccess importing customers!")
    except:
        traceback.print_exc()
        print("\nError importing data!")

def importRMCodes():
    # Import rmCodes
    try:
        
        with open('home/Resources/rmItems2017.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rmCode = row['RMCode']
                rmDescription = row['name']
                rmRef = RMReference(rmCode=rmCode,rmDescription=rmDescription)
                rmRef.save()
                print(rmDescription)
            print("\nSuccess importing rmCodes!")
    except:
        traceback.print_exc()
        print("\nError importing data!")

def importRDProjects():
    # Import RD Projects
    try:
        with open('home/Resources/rdProjects.csv') as csvfile:
            print("File imported!")
            reader = csv.DictReader(csvfile)
            for row in reader:
                subject = row['subject'] 
                customerId = CustomerID.objects.get(id=row['customerInquiry'])
                instruction = row['instruction']
                rdProject = RDProject(subject=subject, customer=customerId, instructions=instruction)
                rdProject.save()
                print(customerId)
        print("\nSuccess importing rdProjects!")
    except:
        traceback.print_exc()
        print("\nError importing data!")

def importBCCOdes():
    # Import BC Codes
    try:
        with open('home/Resources/bcCodes2018.csv') as csvfile:
            print("File imported!")
            reader = csv.DictReader(csvfile)
            for row in reader:
                pCode = row['FormCode']
                pDescription = row['name']
                productType = ProductType(productCode=pCode, productDescription=pDescription)
                productType.save()
                print(pDescription)
        print("Success importing batch codes!")
    except:
        traceback.print_exc()
        print("\nError importing data!")

    # Import PaintInfo
    try:
        with open('home/Resources/paintInfo_Sample.csv') as csvfile:
            print("File imported!")
            reader = csv.DictReader(csvfile)
            errorRow = errorBatchCard = {}
            errBC = errImp = 0
            print("Iteration to begin")
            for row in reader:
                try:
                    batchType = row['paintInfoType']
                    pType = ProductType.objects.get(id=row['productType'])
                    rdP = RDProject.objects.get(id=row['rdProject'])
                    batchPeriod = row['batchPeriod']
                    bNumber = row['batchNumber']
                    iFog = row['iFOG']
                    iVisc = row['initialV']
                    iViscType = row['initialVUnit']
                    fSG = row['finalSG']
                    fHardD = row['fHardDry']
                    fHardDUnit = row['fHardDryUnit']
                    fTouchD = row['fTouchDry']
                    fTouchDUnit = row['fTouchDryUnit']
                    fDFT = row['finalDFT']
                    fDFTUnit = row['finalDFTUnit']
                    fOpacity = row['finalOpacity']
                    fFog = row['fFOG']
                    fVisc = row['finalV']
                    fViscType = row['finalVUnit']
                    fGloss = row['finalGloss']
                    fDE = row['finalDE']
                    fDESpec = row['finalDESpec']
                    dIssued = datetime.strptime(row['dateIssued'], '%m/%d/%Y').strftime("%Y-%m-%d")
                    dLoaded = datetime.strptime(row['dateLoaded'], '%m/%d/%Y').strftime("%Y-%m-%d")
                    dPremixPassed = datetime.strptime(row['datePremixPassed'], '%m/%d/%Y').strftime("%Y-%m-%d")
                    act = row['active']

                    try:
                        paintInfo = PaintInfo(
                            paintInfoType = batchType,
                            productType = pType,
                            rdProject = rdP,
                            batchPeriod = batchPeriod,
                            batchNumber = bNumber,
                            initialFog = iFog,
                            initialViscosity = iVisc,
                            initialViscosityUnit = iViscType,
                            finalSg = fSG,
                            finalHardDry = fHardD,
                            finalHardDryUnit = fHardDUnit,
                            finalTouchDry = fTouchD,
                            finalTouchDryUnit = fTouchDUnit,
                            finalDft = fDFT,
                            finalDftUnit = fDFTUnit,
                            finalOpacity = fOpacity,
                            finalFog = fFog,
                            finalViscosity = fVisc,
                            finalViscosityUnit = fViscType,
                            finalGloss = fGloss,
                            finalColorDe = fDE, 
                            finalColorDeSpec = fDESpec,
                            dateIssued = dIssued,
                            dateLoaded = dLoaded,
                            datePremixPassed = dPremixPassed,
                            active = act,
                            )
                        paintInfo.save()
                        print(paintInfo.productType)
                    except:
                        print('Error importing -> {}'.format(row['batchNumber']))
                        traceback.print_exc('trace.txt')
                        errBC += 1
                        errorBatchCard[err] = row['batchNumber']

                except:
                    print("Error extracting row {}".format(row['batchNumber']))
                    # traceback.print_exc()
                    errImp += 1
                    errorRow[errImp] = row['batchNumber']

        print('\n\n Summary of import -> {} failed file extractions, {} failed object imports'.format(len(errorRow), len(errorBatchCard)))
    except:
        traceback.print_exc()
        print("\nError importing data!")

def deleteAllHome():
    # Import customers
    try:
        UserToDo.objects.all().delete()
        UserNote.objects.all().delete()
        NoteDescription.objects.all().delete()
        print("\nAll BCCOdes deleted!")
    except:
        traceback.print_exc()
        print("\nError deleted data!")
        
def deleteBatchCards():
    # Import customers
    try:
        PaintInfo.objects.all().delete()
        print("\nAll BCCOdes deleted!")
    except:
        traceback.print_exc()
        print("\nError deleted data!")

def deleteDeliveryPlans():
    # Import customers
    try:
        DeliveryPlan.objects.all().delete()
        print("\nAll DeliveryPlan's deleted!")
    except:
        traceback.print_exc()
        print("\nError deleted data!")

def deleteRDProjects():
    # Import customers
    try:
        RDProject.objects.all().delete()
        print("\nAll R&D Projects deleted!")
    except:
        traceback.print_exc()
        print("\nError deleted data!")

def deleteCustomers():
    # Import customers
    try:
        CustomerID.objects.all().delete()
        print("\nAll customers deleted!")
    except:
        traceback.print_exc()
        print("\nError deleted data!")

def deleteRMCodes():
    # Import customers
    try:
        RMReference.objects.all().delete()
        print("\nAll RMCodes deleted!")
    except:
        traceback.print_exc()
        print("\nError deleted data!")

def deleteProductTypes():
    # Import customers
    try:
        ProductType.objects.all().delete()
        print("\nAll ProductType's deleted!")
    except:
        traceback.print_exc()
        print("\nError deleted data!")


# Script to handle commandline communcation
if (__name__ == "__main__"):
    if sys.argv[1] == "importCustomers":
        importCustomers()
    elif sys.argv[1] == "importRMCodes":
        importRMCodes()
    elif sys.argv[1] == "deleteCustomers":
        deleteCustomers()
    elif sys.argv[1] == "deleteRMCodes":
        deleteRMCodes()
    elif sys.argv[1] == "deleteRDProjects":
        deleteRDProjects()
    elif sys.argv[1] == "deleteBatchCards":
        deleteBatchCards()
    elif sys.argv[1] == "deleteDeliveryPlans":
        deleteDeliveryPlans()
    elif sys.argv[1] == "deleteProductTypes":
        deleteProductTypes()
    else:
        print("Method not found!")