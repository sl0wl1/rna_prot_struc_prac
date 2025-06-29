from pathlib import Path
import pandas as pd

def extract_tRNAscan_file(path: str) -> pd.DataFrame:

    records = []

    for folder in Path(path).iterdir():
        if folder.is_dir() and folder.name.endswith('results'):
            
            trna_scan = list(folder.glob('*tRNAscan.txt'))

            if not trna_scan:
                continue  
            
            dir_prefix, dir_suffix = folder.name.split('__')
            dir_suffix = dir_suffix.removesuffix('_results')        

            trna_scan_path = trna_scan[0]
            
            with trna_scan_path.open('r') as f:
                content = f.read()
                entries = [e.strip() for e in content.split('\n\n') if e.strip()]
                for entry in entries:
                    lines = entry.splitlines()
                    if not lines:
                        continue
                    name = lines[0].split()[0]
                    name, trna_n, trna_begin, trna_end, trna_type, anticodon, intron_begin, intron_end, inf_score, hmm_score, two_str_score, isotype_cm, isotype_score, note = None, None, None, None, None, None, None, None, None, None, None, None, None, None
                    for line in lines[3:]:
                        
                        line_split = [split.strip() for split in line.split("\t")]
                        
                        # Some notes are missing, so we check the length of the split line
                        if len(line_split) < 14:
                            line_split.append("") # Append an empty string for the missing note
                            
                        name, trna_n, trna_begin, trna_end, trna_type, anticodon, intron_begin, intron_end, inf_score, hmm_score, two_str_score, isotype_cm, isotype_score, note = line_split
                        
                
                        records.append({
                            'superphyla': dir_prefix,
                            "id": dir_suffix,
                            'name': f"{name}.trna{trna_n}",
                            "trna_begin": trna_begin,
                            "trna_end": trna_end,
                            "trna_type": trna_type,
                            "anticodon": anticodon,
                            "intron_begin": intron_begin,
                            "intron_end": intron_end,
                            "inf_score": inf_score,
                            "hmm_score": hmm_score,
                            "two_str_score": two_str_score,
                            "isotype_cm": isotype_cm,
                            "isotype_score": float(isotype_score),
                            "note": note,          
                        })
    
    return pd.DataFrame(records)
