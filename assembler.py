def assemble(input_file, output_file):

    with open("Pong.asm", "r") as asm_file, open("Pong.hack", "w") as hack_file:
        
        predefined = {
            "R0": 0, 
            "R1": 1, 
            "R2": 2, 
            "R3": 3, 
            "R4": 4, 
            "R5": 5, 
            "R6": 6, 
            "R7": 7,
            "R8": 8, 
            "R9": 9, 
            "R10": 10, 
            "R11": 11, 
            "R12": 12, 
            "R13": 13, 
            "R14": 14, 
            "R15": 15,
            "SCREEN": 16384, 
            "KBD": 24576,
            "SP": 0, 
            "LCL": 1, 
            "ARG": 2, 
            "THIS": 3, 
            "THAT": 4

        }

        comp_bits = {
            "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000",
            "M": "1110000", "!D": "0001101", "!A": "0110001", "!M": "1110001", "-D": "0001111",
            "-A": "0110011", "-M": "1110011", "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
            "D-1": "0001110", "A-1": "0110010", "M-1": "1110010", "D+A": "0000010", "D+M": "1000010",
            "D-A": "0010011", "D-M": "1010011", "A-D": "0000111", "M-D": "1000111", "D&A": "0000000",
            "D&M": "1000000", "D|A": "0010101", "D|M": "1010101"
        }

        dest_bits = {
            None: "000", "M": "001", "D": "010", "MD": "011", "DM": "011", "A": "100",
            "AM": "101", "MA": "101", "AD": "110", "DA": "110", "ADM": "111", "AMD": "111",
            "DAM": "111", "DMA": "111", "MAD": "111", "MDA": "111"
        }

        jump_bits = {
            None: "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100",
            "JNE": "101", "JLE": "110", "JMP": "111"
        }

        label = {}

        variable = {}

        line_count = 0
        asm_file.seek(0)


        #first pass 

        for line in asm_file:   
            line_fir = line.strip()

            if not line_fir or line_fir.startswith("//"):
                continue

            elif ((line_fir.startswith("(") == True and line_fir.endswith(")") == True) or line_fir.isalnum() == True or "_$.:" in line_fir):
                bin_num = format(line_count, '016b')
                label[line_fir[1:-1]] = bin_num


            else:
                line_count+=1
            

        #second pass
        asm_file.seek(0)
        add = 16

        for line in asm_file:
            line_sec = line.strip()

            if line_sec.startswith("@") and line_sec[1:].isdigit():
                value = int(line_sec[1:])
                bin_str = format(value, '016b')
                hack_file.write(bin_str + '\n')

            elif not line_sec or line_sec.startswith("//"):
                continue
            
            
            elif line_sec.startswith("@") and line_sec[1:] in predefined:
                value = predefined[line_sec[1:]]
                bin_num = format(value, '016b')
                hack_file.write(bin_num + '\n')


            elif line_sec.startswith("@") or line_sec.isalnum() == True or "_$.:" in line_sec:
                if line_sec[1:] in label:
                    bin_num = label[line_sec[1:]]
                    hack_file.write(bin_num + '\n')
                else:
                    if line_sec[1:] not in variable:
                        variable[line_sec[1:]] = format(add, '016b')
                        hack_file.write( variable[line_sec[1:]]+ '\n')
                        add+=1
                    else:
                        hack_file.write( variable[line_sec[1:]]+ '\n')
                        
                    


            
            elif "=" in line_sec or ";" in line_sec:
                dest = None
                comp = None
                jump = None
                
                
                if "=" in line_sec:
                    parts = line_sec.split("=")
                    dest = parts[0].strip()
                    comp = parts[1]
                
                
                elif ";" in line_sec:
                    parts = line_sec.split(";")
                    comp = parts[0].strip()
                    jump = parts[1].strip()
                
                
                
                else:
                    comp = line_sec.strip()
                
                
                
                comp_code = comp_bits.get(comp, "0000000")
                dest_code = dest_bits.get(dest, "000")
                jump_code = jump_bits.get(jump, "000")
                bin_num = "111" + comp_code + dest_code + jump_code
                hack_file.write(bin_num + '\n')

    print(label)

assemble("Pong.asm","Pong.hack")
