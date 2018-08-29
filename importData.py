import gspread
from oauth2client.service_account import ServiceAccountCredentials
from importMethods import importRMCodes, importRDProjects, importBCCOdes
from production.models import RMReference
from quality.models import PaintInfo, ProductType, RDProject
from sales.models import CustomerID, DeliveryPlan
import traceback
import sys

BCCODES_SPREADSHEET = "wrangledPaintInfo_afterClean" 
RDPROJECTS_SPREADSHEET = "rdProjects"
DELIVERYPLANS_SPREADSHEET = "deliveryPlans"
PRODUCTCODES_SPREADSHEET = "productCodes"
RMCODES_SPREADSHEET = "rmCodes"
CUSTOMER_SPREADSHEET = "customer2018"

# Get gspread Worksheet object
def getSheet(sheetName):
	try:
		# Scope defines api end point - Use creds to create a client to interact with the Google Drive API
		print("\n-> Trying connection with drive...")
		scope = ['https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
		client = gspread.authorize(creds)
		_ = client.open(sheetName).sheet1

		print("-> Authentication valid.\n")
		print("{} summary:".format(sheetName))
		print('\nrows: {} \ncolumns: {}\n\nRow headings: \n{}\n\n'.format(_.row_count, _.col_count, _.row_values(1)))
		return _
	except:
		traceback.print_exc()
		print("\n-> Authentication failed! \n")
		return False

def importCustomers():
	# Import data from Google Sheets and transfer to django models
	try:
		sheet = getSheet(CUSTOMER_SPREADSHEET)
		column = 0
		countPass = 0
		countFail = 0
		countPass_customer = []
		countFail_customer = []
		# iterate through each list in returned dictionary, return blanks as None
		print("\n-> Starting transfer process.\n")
		for i in sheet.get_all_records(head=1, default_blank=None):
			# print("{}\n".format(i))
			try:
				CustomerID(
					customerCode=i['accCode'],
					customerName=i['accName'],
					customerStatus=i['status'],
					customerType=i['type'],
				).save()
				column = 0
				countPass += 1
				countPass_customer.append(i["accCode"])
				print('{}'.format(CustomerID.objects.last()), end="\r")
			except:
				traceback.print_exc()
				countFail += 1
				countFail_customer.append(i["accCode"])
				print("Error importing {}".format(i["accCode"]), end="\r")
		print('\n\nCustomerID pk range: {}-{}'.format(CustomerID.objects.first().pk, CustomerID.objects.latest('id').pk))
		print("\n\nTransfer process complete. \n\n{} of {} successfully transfered.\n\nFollowing customers failed {}".format(countPass,
			len(sheet.get_all_records(head=1, default_blank=None)), countFail_customer))
	except:
		traceback.print_exc()
		print("\n---ERROR: Unable to import values!")

def importRMCodes():
	# Import data from Google Sheets and transfer to django models
	try:
		sheet = getSheet(RMCODES_SPREADSHEET)
		column = 0

		# iterate through each list in returned dictionary, return blanks as None
		for i in sheet.get_all_records(head=1, default_blank=None):
			# print("{}\n".format(i))
			try:
				RMReference(
					rmCode=i['code'],
					rmDescription=i['description'],
				).save()
				column = 0
				print('{} inserted!'.format(RMReference.objects.last()))
			except:
				traceback.print_exc()
				print("Error importing {} - {}".format(i["code"], i["description"]))
		print('RMReference pk range: {}-{}'.format(RMReference.objects.first().pk, RMReference.objects.latest('id').pk))
	except:
		traceback.print_exc()
		print("\n---ERROR: Unable to import values!")

def importProductTypes():
	# Import data from Google Sheets and transfer to django models
	try:
		sheet = getSheet(PRODUCTCODES_SPREADSHEET)
		column = 0
		countPass = 0
		countPass_productType = []
		countFail = 0
		countFail_productType = []
		# iterate through each list in returned dictionary, return blanks as None
		print("\n-> Starting transfer process.\n")
		for i in sheet.get_all_records(head=1, default_blank=None):
			# print("{}\n".format(i))
			try:
				ProductType(
					productCode=i['productCode'],
					productDescription=i['productDescription'],
				).save()
				column = 0
				countPass += 1
				countPass_productType.append(i["productCode"])
				print('{} inserted!'.format(ProductType.objects.last()))
			except:
				traceback.print_exc()
				countFail += 1
				countFail_productType.append(i["productCode"])
				print("Error importing {} - {}".format(i["Product Code"], i["Product Name"]))
		print('ProductType pk range: {}-{}'.format(ProductType.objects.first().pk, ProductType.objects.latest('id').pk))
	except:
		traceback.print_exc()
		print("\n---ERROR: Unable to import values!")
	print("\n\nTransfer process complete. \n\n{} of {} successfully transfered.\n\nFollowing products failed {}".format(countPass,
			len(sheet.get_all_records(head=1, default_blank=None)), countFail_productType))

def importDeliveryPlans():
	# Import data from Google Sheets and transfer to django models
	try:
		sheet = getSheet(DELIVERYPLANS_SPREADSHEET)
		column = 0

		# iterate through each list in returned dictionary, return blanks as None
		for i in sheet.get_all_records(head=1, default_blank=None):
			# print("{}\n".format(i))
			try:
				DeliveryPlan(
					customerID=CustomerID.objects.get(id=i['customerID']),
					orderDate=i['orderDate'],
					dateOfDelivery=i['dateOfDelivery'],
					invoiceNumber=i['invoiceNumber'],
					active=i['active'],
				).save()
				column = 0
				print('{} inserted!'.format(DeliveryPlan.objects.last()))
			except:
				traceback.print_exc()

				print("Error importing {}".format(CustomerID.objects.get(id=i['subject'])))
		print('DeliveryPlan pk range: {}-{}'.format(DeliveryPlan.objects.first().pk, DeliveryPlan.objects.latest('id').pk))
	except:
		traceback.print_exc()
		print("\n---ERROR: Unable to import values!")

def importRDProjects():
	# Import data from Google Sheets and transfer to django models
	try:
		sheet = getSheet(RDPROJECTS_SPREADSHEET)
		column = 0

		# iterate through each list in returned dictionary, return blanks as None
		for i in sheet.get_all_records(head=1, default_blank=None):
			# print("{}\n".format(i))
			try:
				RDProject(
					subject=i['subject'], 
					customer=CustomerID.objects.get(id=i['customerInquiry']), 
					instructions=i['instruction']
				).save()

				column = 0
				print('{} inserted!'.format(RDProject.objects.last()))
			except:
				traceback.print_exc()
				print("Error importing {}".format(i["subject"]))

		print('RDProject pk range: {}-{}'.format(RDProject.objects.first().pk, RDProject.objects.latest('id').pk))
	except:
		traceback.print_exc()
		print("\n---ERROR: Unable to import values!")

def importBatchCards():
	# Import data from Google Sheets and transfer to django models
	try:
		sheet = getSheet(BCCODES_SPREADSHEET)
		column = 0
		countPass = 0
		countFail = 0
		countPass_batch = []
		countFail_batch = []
		
		# iterate through each list in returned dictionary, return blanks as None
		print("\n-> Starting transfer process.\n")
		for i in sheet.get_all_records(head=1, default_blank=None):
			# print("{}\n".format(i))
										
			# identify  column in list i and allocate to model field
			try:
				PaintInfo(
					paintInfoType = i["paintInfoType"],
					premixMachine = i["premixMachine"],
		            productType = ProductType.objects.get(productCode=i["productCode"]),
		            rdProject = None if i["rdProject"] == None else RDProject.objects.get(id=i["rdProject"]),
		            batchPeriod = i["batchPeriod"],
		            batchNumber = i["batchNumber"],
		            initialFog = i["premixFOG"],
		            initialPremixViscosity = i["premixInitialViscosity"],
		            finalPremixViscosity = i["premixViscosity"],
		            initialViscosityUnit = "KU",
		            finalSg = i["finalSG"],
		            finalHardDry = i["finalHardDry"],
		            finalHardDryUnit = i["finalHardDryUnit"],
		            finalTouchDry = i["finalTouchDry"],
		            finalTouchDryUnit = i["finalTouchDryUnit"],
		            finalDft = i["finalDFT"],
		            finalOpacity = i["finalOpacity"],
		            finalFog = i["finalFOG"],
		            finalViscosity = i["finalBatchViscosity"],
		            finalViscosityUnit = i["finalBatchViscosityUnit"],
		            finalGloss = i["finalGloss"],
		            finalColorDe = i["finalDE"],
		            finalColorDeSpec = i["finalDESpec"],
		            dateIssued = i["dateBatchIssued"],
		            dateLoaded = i["premixDateLoaded"],
		            datePremixPassed = i["premixDatePassed"],
		            active = i["active"],
					).save()
				column = 0
				countPass += 1
				countPass_batch.append(i["batchNumber"])
				print('{} inserted!'.format(PaintInfo.objects.last()), end="\r")
			except:
				traceback.print_exc()
				print("Error importing {}".format(i["batchNumber"]), end="\r")
				countFail += 1
				countFail_batch.append(i["batchNumber"])
		print("\n\nTransfer process complete. \n\n{} of {} successfully transfered.\n\nFollowing batch cards failed {}".format(countPass,
			len(sheet.get_all_records(head=1, default_blank=None)), countFail_batch))
	except:
		traceback.print_exc()
		print("\n---ERROR: Unable to import values!")

# Script to handle commandline communcation
if (__name__ == "__main__"):
	if (sys.argv[1] == "importBatchCards"):
	    importBatchCards()
	elif sys.argv[1] == "importRDProjects":
	    importRDProjects()
	elif sys.argv[1] == "importDeliveryPlans":
	   	importDeliveryPlans()
	elif sys.argv[1] == "importProductTypes":
	   	importProductTypes()
	elif sys.argv[1] == "importRMCodes":
	   	importRMCodes()
	elif sys.argv[1] == "importCustomers":
	   	importCustomers() 
	else:
	    print("Method not found!")