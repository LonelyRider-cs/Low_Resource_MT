import sentencepiece as spm
import os, sys

def sentencepiece_train(training_file_name: str, model_prefix: str, model_type: str='bpe', vocab_size: int=16000, user_defined_symbols=[]):
    """
    train a tokenization model implemented in sentencepiece, default is BPE
    """
    spm.SentencePieceTrainer.train(input=training_file_name,
                                   model_prefix=model_prefix,
                                   vocab_size=vocab_size,
                                   user_defined_symbols=user_defined_symbols,
                                   model_type=model_type)

def sentencepiece_segment(text: str, model_file_name: str) -> str:
    # segmentation
    sp = spm.SentencePieceProcessor(model_file=model_file_name)
    text_bpe = sp.encode(text, out_type=str)
    text_bpe = " ".join(text_bpe)
    return text_bpe

def main():
    language = sys.argv[1]
    training_file_name = sys.argv[2]
    model_dir = 'bpe_models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_prefix = model_dir + '/' + language
    model_type = 'bpe'
    # vocab_size = 8000
    vocab_size = 50
    user_defined_symbols = []
    sentencepiece_train(training_file_name=training_file_name,
                        model_prefix=model_prefix,
                        model_type=model_type,
                        vocab_size=vocab_size,
                        user_defined_symbols=user_defined_symbols)

    model_file_name = model_prefix + '.model'
    out_dir = 'data_bpe/'+language
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    fout_name = os.path.join(out_dir, language+'.txt')
    with open(training_file_name) as f, open(fout_name, 'w') as fw:
        for line in f:
            text_bpe = sentencepiece_segment(line.strip(), model_file_name)
            fw.write(text_bpe+'\n')

if __name__ == "__main__":
    main()