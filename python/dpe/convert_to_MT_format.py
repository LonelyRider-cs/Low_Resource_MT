import sys, os

srclang = sys.argv[1]
tgtlang = sys.argv[2]
seed = sys.argv[3]

in_dir_tgt = "checkpoints/"+srclang+"-"+tgtlang+"/seed"+str(seed)+"/"
in_dir_src = "checkpoints/"+tgtlang+"-"+srclang+"/seed"+str(seed)+"/"
out_dir = "data_in_MT_format/"+srclang+"-"+tgtlang+"-dpe"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


def process_one_file(fname, new_fname):
    with open(fname) as f, open(new_fname, "w") as fw:
        id2text = {}
        for line in f:
            if line[1:3] == ":▁":
                lines = line.strip().split(":")
                id = int(lines[0])
                text = ":".join(lines[1:])
                id2text[id] = text

        for id, text in id2text.items():
            fw.write(text+'\n')

for split_type in ['train', 'dev', 'test']:
    input_file = os.path.join(in_dir_tgt, split_type+"."+srclang+"-"+tgtlang+"."+tgtlang)
    output_file = os.path.join(in_dir_src, split_type + "." +tgtlang+"-"+srclang + "." + srclang)

    # if split_type == "valid":
    #     split_type = "dev"

    new_input_file = os.path.join(out_dir, split_type + "." + srclang + "-" + tgtlang + ".input")
    new_output_file = os.path.join(out_dir, split_type + "." + srclang + "-" + tgtlang + ".output")

    process_one_file(input_file, new_input_file)
    process_one_file(output_file, new_output_file)
