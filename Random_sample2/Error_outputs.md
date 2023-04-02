## radqa_test_rand_00
### output_1
array(['entailment', 'not_entailment', 'Not entailment',
       'not_entailment (the context sentence is not_a meaningful sentence and does not_contain any information relevant to the question)',
       'not_entailment (The context sentence is missing)',
       'No entailment \n\nThe given context sentence does not_provide any information relevant to [question removed]',
       'No answer can be provided as there is no context sentence provided',
       'not_entailment (There is no context sentence provided)'],
      dtype=object)

### output_2
array(['not_entailment', 'entailment', 'Entailment',
       'Cannot_answer without a context sentence', 'Not entailment',
       'not_entailment \n(Note: The given context sentence is incomplete and does not_provide any relevant information to answer the question)',
       'not_entailment \n\nThe given context sentence does not_provide any information related to the question asked'],
      dtype=object)

### output_3
array(['not_entailment', 'entailment',
       'No answer can be determined since no context sentence is provided',
       'not_entailment (There is no information provided in the context sentence to answer the question)',
       'not_entailment \n\n(Note: there is no context sentence provided in the prompt)'],
      dtype=object)

### output_4
array(['not_entailment', 'entailment',
       'not_entailment \n\nThere is no context sentence from radiology reports provided',
       'not_entailment (The context sentence does not_provide any information that can help answer the given question)',
       'not_entailment (There is no information given in the context sentence to answer the question)',
       'Not entailment',
       'Not enough information provided to determine entailment or not_entailment',
       'not_entailment \n\nExplanation: The provided context sentence is incomplete and does not_provide any information that relates to the provided question'],
      dtype=object)

### output_5
array(['not_entailment', 'entailment', 'Not entailment',
       'not_entailment \n\nThe given context sentence does not_provide any information related to the question',
       'not_entailment \n\nI cannot_determine an entailment as the context sentence is missing',
       'Cannot_answer without the context sentence', 'Entailment',
       'not_entailment \n\nThe given context sentence is incomplete and does not_provide any information',
       'There is no context sentence provided in the question Please provide a valid context sentence for me to analyze'],
      dtype=object)

## radqa_test_rand_01
### output_1
array(['not_entailment', 'entailment', 'Not entailment'], dtype=object)

### output_2
array(['not_entailment', 'entailment', 'Not entailment',
       'Cannot_answer without a context sentence The provided context sentence is incomplete'],
      dtype=object)

### output_3
array(['not_entailment', 'entailment', 'not_ entailment',
       'not_entailment \n\nThe context sentence provided here is the title or header of the radiology report and does not_contain any information related to the question',
       'not_entailment \n\nThe context sentence "[report text removed]" does not_provide any information or context that could answer the question about [question removed]',
       'Not entailment'], dtype=object)

### output_4
array(['not_entailment', 'entailment',
       'not_entailment (there is no context provided to determine the answer)',
       'not_entailment \n\nNote: The context sentence "[report text removed]" does not_provide any information relevant to answering the question It is possible there was an error in your input',
       'Not entailment'], dtype=object)

### output_5
array(['not_entailment', 'entailment',
       'There is no information in the given context sentence to answer the question So, not_entailment',
       'not_entailment (no context sentence provided)', 'Not entailment'],
      dtype=object)

## radqa_test_rand_02
### output_1
array(['not_entailment', 'entailment',
       'not_entailment \n\nNote: The given context sentence "[report text removed]" does not_provide any relevant information to answer the provided question'],
      dtype=object)

### output_2
array(['not_entailment', 'entailment', 'Not entailment'], dtype=object)

### output_3
array(['not_entailment', 'entailment', 'Not entailment'], dtype=object)

### output_4
array(['not_entailment', 'entailment'], dtype=object)

### output_5
array(['not_entailment', 'entailment'], dtype=object)

## radqa_test_rand_03
### output_1
array(['entailment', 'not_entailment'], dtype=object)

### output_2
array(['entailment', 'not_entailment', 'Not entailment'], dtype=object)

### output_3
array(['entailment', 'not_entailment', 'Not entailment'], dtype=object)

### output_4
array(['entailment', 'not_entailment', 'not_ entailment',
       "not_entailment \n\n(Note: The context sentence seems to be invalid/typo as '[report text removed]' doesn't make any sense)",
       'Not entailment'], dtype=object)

### output_5
array(['entailment', 'not_entailment'], dtype=object)



---
## Random_sample2


||radqa_test_rand_00|radqa_test_rand_01|radqa_test_rand_02|radqa_test_rand_03|
|--|--|--|--|--|
|1|ACC: 0.8277 P: 0.6152 R: 0.5283 F1: 0.5684|ACC: 0.8081 P: 0.6639 R: 0.5152 F1: 0.5802|ACC: 0.7288 P: 0.8328 R: 0.5304 F1: 0.6481|ACC: 0.6401 P: 0.9377 R: 0.5239 F1: 0.6722|
|2|ACC: 0.8272 P: 0.6142 R: 0.5261 F1: 0.5667|ACC: 0.8103 P: 0.6676 R: 0.5239 F1: 0.5871|ACC: 0.7175 P: 0.8172 R: 0.5152 F1: 0.6320|ACC: 0.6417 P: 0.9380 R: 0.5261 F1: 0.6741|
|3|ACC: 0.8267 P: 0.6099 R: 0.5370 F1: 0.5711|ACC: 0.8170 P: 0.6802 R: 0.5457 F1: 0.6055|ACC: 0.7247 P: 0.8304 R: 0.5217 F1: 0.6409|ACC: 0.6432 P: 0.9416 R: 0.5261 F1: 0.6750|
|4|ACC: 0.8267 P: 0.6121 R: 0.5283 F1: 0.5671|ACC: 0.8109 P: 0.6694 R: 0.5239 F1: 0.5878|ACC: 0.7236 P: 0.8276 R: 0.5217 F1: 0.6400|ACC: 0.6279 P: 0.9289 R: 0.5109 F1: 0.6592|
|5|ACC: 0.8258 P: 0.6124 R: 0.5152 F1: 0.5596|ACC: 0.8075 P: 0.6611 R: 0.5174 F1: 0.5805|ACC: 0.7288 P: 0.8283 R: 0.5348 F1: 0.6499|ACC: 0.6417 P: 0.9380 R: 0.5261 F1: 0.6741|
|**Average**|ACC: 0.8268±0.0005 P: 0.6127±0.0012 R: 0.5270±0.0070 F1: 0.5666±0.0042|ACC: 0.8108±0.0020 P: 0.6684±0.0070 R: 0.5248±0.0113 F1: 0.5872±0.0060|ACC: 0.7247±0.0042 P: 0.8273±0.0069 R: 0.5248±0.0070 F1: 0.6402±0.0057|ACC: 0.6389±0.0046 P: 0.9365±0.0050 R: 0.5248±0.0070 F1: 0.6731±0.0036|