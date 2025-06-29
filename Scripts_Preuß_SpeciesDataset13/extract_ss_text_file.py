from pathlib import Path
import pandas as pd

def extract_ss_text_file(path: str) -> pd.DataFrame:
    
    records = []


    for folder in Path(path).iterdir():

        if folder.is_dir() and folder.name.endswith('results'):
            ss_files = list(folder.glob('*ss.txt'))
            
            if not ss_files:
                continue
            
            dir_prefix, dir_suffix = folder.name.split('__')
            dir_suffix = dir_suffix.removesuffix('_results')  
            ss_path = ss_files[0]
            
            with ss_path.open('r') as f:
                content = f.read()
                entries = [e.strip() for e in content.split('\n\n') if e.strip()]
                
                for entry in entries:
                    lines = entry.splitlines()
                    if not lines:
                        continue
                    name = lines[0].split()[0]
                    
                    # Assign None or empty list if there is nothing to parse. The code will not break.
                    type_as, anticodon, seq, intron_pos_rel, intron_pos_abs, sec_str = None, None, None, [], [], None
                    possible_intron_counter = 0
                
                    for line in lines[1:]:                    
                        
                        if line.startswith('Type:'):
                            
                            _,type_as,anticodon,*_= line.split(' ')
                        
                            type_as = type_as.split("\t")[0].strip()
                            anticodon = anticodon.strip()
                            
                        elif line.startswith('Seq:'):
                            
                            seq = line.split(':', 1)[1].strip()
                            
                        if line.startswith("Possible intron:"):
                            *_, temp_intron_pos_rel, temp_intron_pos_abs = line.split(" ")
                            temp_intron_pos_rel = [int(pos) for pos in temp_intron_pos_rel.split("-")]
                            temp_intron_pos_abs.replace("(", "").replace(")", "")
                            temp_intron_pos_abs = [int(pos) for pos in temp_intron_pos_abs.replace("(", "").replace(")", "").split("-")]
                            
                            intron_pos_rel.append(temp_intron_pos_rel)
                            intron_pos_abs.append(temp_intron_pos_abs)
                            
                            possible_intron_counter += 1
                            
                        if line.startswith("Str:"):
                            sec_str = line.split(" ")[1].strip()  
                            sec_str = sec_str.translate(str.maketrans({'<': ')', '>': '('})).strip()
                            
                            
                            
                
                    records.append({
                        'superphyla': dir_prefix,
                        "id": dir_suffix,
                        'name': name,
                        'type': type_as,
                        'anticodon': anticodon,
                        'seq': seq,
                        "length": len(seq) if seq else None,
                        "possible_intron_n": possible_intron_counter,
                        "possible_intron_rel": intron_pos_rel,
                        "possible_intron_abs": intron_pos_abs,
                        "dot_bracket_sec_str": sec_str,                
                        })

    return pd.DataFrame(records)
    

