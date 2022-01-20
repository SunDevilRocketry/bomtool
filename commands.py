### Commands.py -- module with all BOM command line functions 
### Author: Colton Acosta
### Date: 1/18/2021
### Sun Devil Rocketry Avionics

# Standard Imports
import sys
from datetime import date
import time

## Production BOM Basic Data

# Convert Numbers to Letters
ExcelCols = ['Null', 'A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

# Table Headers
prodBomHead = ['Item No.', 'Designator', 'Qty','Manufacturer', 'Mfg Part No.', 
                'Description/Value', 'Package/Footprint', 'Type', 'Notes']
# Number of header rows 
prodBomHeadRows = 7

# Table Colors 
lightColor = {
                 "backgroundColorStyle": {
                    "rgbColor": {
                        "red": 256 - 239,
                        "green": 256 - 239,
                        "blue": 256 - 239,
                     }
                  }
               }
darkColor = {
                "backgroundColorStyle": {
                    "rgbColor": {
                        "red": 256 - 204,
                        "green": 256 - 204,
                        "blue": 256 - 204
                     }
                  }
             }


# exitFunc -- quits the program
def exitBOM(bom):
   sys.exit()

# helpFunc -- displays list of commands
def helpFunc(bom):
    print('BOM Tool Commands: \n')

# newProdBom -- creates new production bom
# input: bom spreadsheet object
def newProdBom(bom):

   # Design BOM
   designBom = bom.sheet1

   # create the new sheet
   prodBom = bom.add_worksheet(title="Production BOM", rows="100", cols="20") 

   # Generate Header
   prodBom.merge_cells("A1:I2")
   prodBom.merge_cells("B3:I6", 'MERGE_ROWS')
   prodBom.update("A7:I7", [prodBomHead])
   title = designBom.acell("A1").value.split()
   title.insert(-1, "Production")
   title = ' '.join(title)
   prodBom.update("A1", title)
   prodBom.format("A1", {"textFormat": {"bold": True,
                         "fontSize": 18}})
   designHeadData = designBom.batch_get(["A3:B6"])
   prodBom.update("A3:B6", designHeadData[0])
   today = date.today().strftime("%m/%d/%Y")
   prodBom.update("B5", today)
   prodBom.format("A1:I7", {
                              "borders": {
                                  "top": {
                                      "style": "SOLID"
                                  },
                                  "bottom": {
                                      "style": "SOLID"
                                  },
                                  "left": {
                                      "style": "SOLID"
                                  },
                                  "right": {
                                      "style": "SOLID"
                                  }
                              } 
                           })
   prodBom.format("A1:I6", lightColor)
   prodBom.format("A7:I7", darkColor)

   ## Loop over components and add data

   # Pull headers to determine target column numbers
   designHeaders = designBom.row_values(prodBomHeadRows)

   # Assign Each header a column number
   designHeaderMap = [4, 0, 2, 3, 1, 5, 6]
   baseDesignRow = 8
   designNumParts = len(designBom.col_values(1)) -8
   designTableA = ['A8:G'+str(len(designBom.col_values(1)))]
   partData = designBom.batch_get(designTableA)[0]
   prodPartData = []
   for row in partData:
       if len(row) == 7:
          prodPartData.append(list(row))
          for count, col in enumerate(designHeaderMap):
              prodPartData[-1][count] = row[col]

   # Write Data from lists to spreadsheet
   prodTableA = 'B8:H'+str(baseDesignRow+len(prodPartData))
   prodBom.update(prodTableA, prodPartData)
   itemNos = [*range(1, len(prodPartData)+1)] 
   itemNosV = [[x] for x in itemNos]
   prodFinalRow = baseDesignRow+len(prodPartData)-1
   itemNosTableA = 'A8:A'+str(prodFinalRow)
   prodBom.update(itemNosTableA, itemNosV)
   prodBom.format(itemNosTableA, {"horizontalAlignment": "LEFT"})
   
   # Add background color
   prodPartDataTableA = 'A8:I'+str(prodFinalRow)
   prodBom.format(prodPartDataTableA, {
                              "borders": {
                                  "top": {
                                      "style": "SOLID"
                                  },
                                  "bottom": {
                                      "style": "SOLID"
                                  },
                                  "left": {
                                      "style": "SOLID"
                                  },
                                  "right": {
                                      "style": "SOLID"
                                  }
                              } 
                           })
   prodPartsTableA = 'A8:I'+str(prodFinalRow)
   prodBom.format(prodPartsTableA, lightColor)

   # Make every other row dark
   row = 9 
   while row <= prodFinalRow:
       prodRowTablesA = 'A'+str(row)+':I'+str(row)
       row+=2
       prodBom.format(prodRowTablesA, darkColor)
   # Write Marker Data to random cell to indicate bom 
   # was auto-generated
   prodBom.update("T100", "AUTO-GENERATED")

   # exit
   return(None)


# editProdBom -- updates production BOM to 
#                reflect recent changes to 
#                BOM
def editProdBom(bom):
    return None

# prodBOM -- creates production BOM
# input: bom spreadsheet object
def prodBOM(bom):
    print("Creating Production BOM ...")

    # Check if production BOM exists and/or
    # create new sheet
    # New sheet --> Generate new template 
    #             - Add data to header
    # Existing sheet --> Update new fields
    numsheets = len(bom.worksheets())
    if (numsheets == 1): # New Production BOM
        newProdBom(bom)
    elif(numsheets == 2): # Existing Production BOM
        editProdBom(bom)
    else: # too many sheets
        print("""Error: Too many BOM sheets. Check that
                there are no extra sheets in the BOM.""")

    print("Production BOM successfully created")

# Command List
commands = { "exit": exitBOM,
             "production": prodBOM,
             "help": helpFunc
        }

# parseInput -- checks user input against command list 
#               options
# input: userin: user inputed string
#        bom: spreadsheet object
# output: none
def parseInput(userin, bom): 

    # Get rid of any whitespace
    userin.strip()

    # Check if user input corresponds to a function
    for command in commands: 
        if userin == command:
           commands[command](bom)
           return None

    # User input doesn't correspond to a command
    print("Invalid BOM command")
    userin = input("BOM> ")
    parseInput(userin, bom)

