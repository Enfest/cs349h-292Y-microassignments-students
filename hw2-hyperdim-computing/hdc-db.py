from hdc import *
import csv


class HDDatabase:

    def __init__(self):
        self.db = HDItemMem("db")
        # raise Exception("other instantiations here")
        self.field_codebooks = HDCodebook("field_codebooks")
        self.value_codebooks = HDCodebook("value_codebooks")
        self.string_codebooks = HDCodebook("string_codebooks")

    def encode_string(self, value):
        # raise Exception("translate a string to a hypervector")
        if self.string_codebooks.has(value):
            return self.string_codebooks.get(value)
        else:
            return self.string_codebooks.add(value)

    def decode_string(self, hypervec):
        # raise Exception("translate a hypervector to a string")
        return self.string_codebooks.wta(hypervec)

    def encode_row(self, fields):
        # raise Exception("translate a dictionary of field-value pairs to a hypervector")
        # create a hypervector from the fields
        elements = []
        for field, value in fields.items():
            field_hv = np.array([])
            value_hv = np.array([])
            if self.field_codebooks.has(field):
                field_hv = self.field_codebooks.get(field)
            else:
                field_hv = self.field_codebooks.add(field)
            if self.value_codebooks.has(value):
                value_hv = self.value_codebooks.get(value)
            else:
                value_hv = self.value_codebooks.add(value)
            elements.append(HDC.bind(field_hv, value_hv))

        return HDC.bundle(elements)
            

    def decode_row(self, hypervec):
        # raise Exception("reconstruct a dictionary of field-value pairs from a hypervector.")
        fields = {}
        for key in self.field_codebooks.all_keys():
            key_hv = self.field_codebooks.get(key)
            decode_hv = HDC.bind(key_hv, hypervec)
            value = self.value_codebooks.wta(decode_hv)
            fields[key] = value
        return fields

    def add_row(self, primary_key, fields):
        # raise Exception("add a database row.")
        # create a hypervector from the fields
        hv = self.encode_row(fields)
        # add the hypervector to the database
        self.db.add(primary_key, hv)


    def get_row(self, key):
        # raise Exception("retrieve a dictonary of field-value pairs from a hypervector row")
        hv = self.db.get(key)
        return self.decode_row(hv)

    def get_value(self, key, field):
        # raise Exception("given a primary key and a field, get the value assigned to the field")
        hv = self.db.get(key)
        fields = self.decode_row(hv)
        return {field: fields[field]}

    def get_matches(self, field_value_dict, threshold=0.4):
        hv = self.encode_row(field_value_dict)
        distances = self.db.distance(hv)
        return {
            key: dist
            for key, dist in distances.items()
            if dist < threshold
        }


        

    def get_analogy(self, target_key, other_key, target_value):
        # raise Exception("analogy query")
        target_row = self.db.get(target_key)
        other_row = self.db.get(other_key)
        target_value = self.value_codebooks.get(target_value)
        field = self.field_codebooks.wta(HDC.bind(target_value, target_row))
        field_hv = self.field_codebooks.get(field)
        output_value = self.value_codebooks.wta(HDC.bind(field_hv, other_row))
        return output_value, HDC.dist(HDC.bind(field_hv, other_row), self.value_codebooks.get(output_value))

def load_json():
    data = {}
    with open("digimon.csv", "r") as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['Digimon']
            data[key] = rows
    return data

def build_database(data):
    HDC.SIZE = 10000
    db = HDDatabase()

    for key, fields in data.items():
        db.add_row(key, fields)

    return db


def summarize_result(data, result, summary_fn, verbose=True):
    print("---- # matches = %d ----" % len(list(result.keys())))
    if verbose:
        for digi, distance in result.items():
            print("%f] %s: %s" % (distance, digi, summary_fn(data[digi])))
    else:
        true_matches = 0
        total_matches = len(result.keys())
        for digi, distance in result.items():
            if summary_fn(data[digi]) == "true match":
                true_matches += 1
        print("true matches=%d, false matches=%d" % (true_matches, len(result.keys()) - true_matches))


def digimon_basic_queries(data, db):

    print("===== virus-plant query =====")
    thr = 0.40
    digis = db.get_matches({"Type": "Virus", "Attribute": "Plant"}, threshold=thr)
    summarize_result(data, digis, lambda row: "true match" if row["Type"] == "Virus" and row["Attribute"] == "Plant" else "false positive")

    print("===== champion query =====")
    thr = 0.40
    digis = db.get_matches({"Stage": "Champion"}, threshold=thr)
    summarize_result(data, digis, lambda row: "true match" if row["Stage"] == "Champion" else "false positive")

def digimon_thres_testing_queries(data, db):
    for thres in [0.4, 0.41, 0.42, 0.43, 0.44, 0.45]:
        print("threshold=%f" % thres)
        print("===== virus-plant query =====")
        digis = db.get_matches({"Type": "Virus", "Attribute": "Plant"}, threshold=thres)
        summarize_result(data, digis, lambda row: "true match" if row["Type"] == "Virus" and row["Attribute"] == "Plant" else "false positive", verbose=False)
        print("===== champion query =====")
        digis = db.get_matches({"Stage": "Champion"}, threshold=thres)
        summarize_result(data, digis, lambda row: "true match" if row["Stage"] == "Champion" else "false positive", verbose=False)
        print("---")
def digimon_test_encoding(data, db):
    strn = "tester"
    hv_test = db.encode_string(strn)
    rec_strn = db.decode_string(hv_test)
    print("original=%s" % strn)
    print("recovered=%s" % rec_strn)
    print("---")

    row = data["Wormmon"]
    hvect = db.encode_row(row)
    rec_row = db.decode_row(hvect)
    print("original=%s" % str(row))
    print("recovered=%s" % str(rec_row))
    print("---")


def digimon_value_queries(data, db):
    value = db.get_value("Lotosmon", "Stage")
    print("Lotosmon.Stage = %s" % value)

    targ_row = db.get_row("Lotosmon")
    print("Lotosmon" + str(targ_row))


def analogy_query(data, db):
    # Lotosmon is to Data as Imperialdramon PM is to <what field>

    targ_row = db.get_row("Lotosmon")
    other_row = db.get_row("Imperialdramon PM")
    print("Lotosmon has a a field with a Data value, what is the equivalent value in Imperialdramon PM's entry")
    value, dist = db.get_analogy(target_key="Lotosmon", other_key="Imperialdramon PM", target_value="Data")
    print("Lotosmon" + str(targ_row))
    print("Imperialdramon PM" + str(other_row))
    print("------")
    print("value: %s (dist=%f)" % (value, dist))
    print("expected result: Vaccine, the type of Imperialdramon PM")
    print("")


if __name__ == '__main__':
    data = load_json()
    db = build_database(data)
    # digimon_test_encoding(data, db)
    # digimon_basic_queries(data, db)
    # digimon_value_queries(data, db)
    # digimon_thres_testing_queries(data, db)
    # digimon_test_encoding(data, db)
    analogy_query(data, db)
