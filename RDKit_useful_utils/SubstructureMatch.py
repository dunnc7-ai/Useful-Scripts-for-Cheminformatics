from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw


# Load the molecular library
sdf_file = input("What is the file name of the library to search? ").strip()
if not sdf_file.lower().endswith(".sdf"):
    sdf_file += ".sdf"

supplier = Chem.SDMolSupplier(sdf_file)


with Chem.SDMolSupplier(supplier) as suppl:
	ms = [x for x in suppl if x is not None] 

if not molecules:
    print("No valid molecules found in the SDF file.")
    return

for m in ms: tmp=AllChem.Compute2DCoords(m)

substruct = Chem.MolFromSmiles(input('Paste Substructure Smiles Here: '))

if substruct is None:
    print("Invalid SMILES string.")

subms = [x for x in ms if x.HasSubstructMatch(substruct)]
print(f"Found {len(subms)} matching molecules.")

# Create molecule labels
legends = [
    mol.GetProp("_Name") if mol.HasProp("_Name") else f"Molecule {i + 1}"
    for i, mol in enumerate(subms)
]

# Generate the molecular grid image
img = Draw.MolsToGridImage(
    subms,
    molsPerRow=4,
    subImgSize=(200, 200),
    legends=legends
)

# Save the image
output_file = input("Name of PNG file: ").strip()

if not output_file.lower().endswith(".png"):
    output_file += ".png"

img.save(output_file)

print(f"Image saved as {output_file}")
