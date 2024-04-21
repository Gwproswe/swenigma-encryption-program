import os
import random
import secrets
import time
import hashlib
import uuid
import json
import types
import multiprocessing
import math
import signal
class swenigma:
    def __init__(self,default_keyset=[0,0,0,0,0,['x'],['x'],['x'],['x'],['x']],fail_function=0,processes=4):
        self.processes = processes
        self.fail_function = fail_function
        self.default_keyset = default_keyset
        self.keysets = {}
        self.fail_safe_status = 'on'
        self.message_list = []
        self.key1 = 0
        self.key5 = 0
        self.input = []
        self.outputs = []
        self.outputs_2 = []
        self.outputs_3 = []
        self.outputs_4 = []
        self.vkeys_1 = []
        self.vkeys_2 = []
        self.org_key2 = 0
        self.org_key3 = 0
        self.org_key4 = 0
        if __name__ == '__main__':
            pass
    #fail safe functions
    def fail_safe(self,error):
        if type(self.fail_function) == types.FunctionType:
            self.fail_function(error)
        while True:
            pass
    def enable_failsafe(self):
        self.fail_safe_status = 'on'
    def disable_failsafe(self):
        self.fail_safe_status = 'off'
    #factory functions
    def encrypt_function(self,keyset,message,option = 'ST',time_precsion = 0):
        self.message_list = []
        instance = os.getpid()
        if len(message)<10:
            print('message must be longer then 9')
            return
        self.key1 = keyset[0]
        self.key2 = keyset[1]
        self.key3 = keyset[2]
        self.key4 = keyset[3]
        self.key5 = keyset[4]
        self.inputs = keyset[5]
        self.outputs = keyset[6]
        self.outputs_2 = keyset[7]
        self.outputs_3 = keyset[8]
        self.outputs_4 = keyset[9]
        self.vkeys_1 = []
        self.vkeys_2 = []
        self.message_list = []
        md = len(message)
        md = md - (len(message)%10)
        md = md/10
        if len(message)%10 != 0:
            md = md + 1
        print(md)
        if option == 'ST':
            unique_hash_1 = self.generate_unique_number()
            unique_number_1 = self.convert_letters_to_numbers(unique_hash_1)
            random.seed(unique_number_1+self.key1+self.key4)
            self.message_list.append(str(unique_number_1))
            self.message_list.append('|')
        else:
            print('option error')
        vkey_1_genetator = random.randint(self.key2,self.key3)
        random.seed(vkey_1_genetator)
        for i in range(0,int(md)):
            self.vkeys_1.append(random.randint(round(self.key2/10),round(self.key2/2)))
        unique_hash_2 = self.generate_unique_number()
        unique_number_2 = self.convert_letters_to_numbers(unique_hash_2)
        random.seed(unique_number_2+self.key1+self.key4)
        self.message_list.append(str(unique_number_2))
        self.message_list.append('|')
        vkey_2_genetator = random.randint(self.key2,self.key3)
        random.seed(vkey_2_genetator)
        for i in range(0,int(md)):
            self.vkeys_2.append(random.randint(0+self.key2,2000+self.key2*self.key3*self.key1*self.key4))
        self.org_key2 = self.key2
        self.org_key3 = self.key3
        self.org_key4 = self.key4
        proc = []
        for i in range(0,self.processes):
            proc.append(multiprocessing.Process(target=self.core_encryption_function, args=(math.ceil(i*md/self.processes),math.ceil((i+1)/self.processes*md),message,instance,),name=str(i)))
        for p in proc:
            p.start() 
        for p in proc:
            p.join()
        for i in range(0,self.processes):
            f = open(f"swenigma_process_encryption_{i}_output_{instance}.txt",'r')
            content = f.readlines(0)
            output = ''.join(content)
            f.close()
            os.remove(f"swenigma_process_encryption_{i}_output_{instance}.txt")
            self.message_list.append(output)
        x = ''.join(self.message_list)
        return x
    def encode(self,message):
        result = ''
        for x in message:
            output = random.randint(1,4)
            if output == 1:
                    index = self.inputs.index(x)
                    result = result + self.outputs[index]
            elif output == 2:
                    index = self.inputs.index(x)
                    result = result + self.outputs_2[index]
            elif output == 3:
                    index = self.inputs.index(x)
                    result = result + self.outputs_3[index]
            elif output == 4:
                    index = self.inputs.index(x)
                    result = result + self.outputs_4[index]
        return result
    def add_salt(self,message,key2,key3,key4):
        salting_complete = 0
        salting_table = []
        for x in message:
            salting_table.append(x)
        random.seed(key4)
        salting_table.insert(random.randint(0, len(salting_table)), random.choice(self.inputs))
        keys = key2
        while salting_complete != 2:
            random.seed(key4-keys)
            salting_table.insert(random.randint(0, len(salting_table)), random.choice(self.outputs))
            random.seed(key4+keys)
            salting_table.insert(random.randint(0, len(salting_table)), random.choice(self.outputs_2))
            random.seed(key4*keys)     
            salting_table.insert(random.randint(0, len(salting_table)), random.choice(self.outputs_3))
            random.seed(key4-keys-keys)
            salting_table.insert(random.randint(0, len(salting_table)), random.choice(self.outputs_4))
            keys = key3
            salting_complete = salting_complete + 1
        return ''.join(salting_table)
    def generate_unique_number(self):
        system_info = uuid.getnode()
        current_time = int(time.time())
        unique_identifier = str(uuid.uuid4())
        combined_data = str(system_info).encode() + str(current_time).encode() + str(unique_identifier).encode()
        unique_hash = hashlib.sha256(combined_data).hexdigest()
        return unique_hash
    def convert_letters_to_numbers(self,input_string):
        converted_string = ""
        for char in input_string:
            if char.isalpha():
                converted_char = str(ord(char.upper()) - 64)
                converted_string += converted_char
            else:
                converted_string += char
        return int(converted_string)
    def core_encryption_function(self,start,end,message,instance):
        chunck_list = []
        print('k')
        for y in range(int(start),int(end)):
            vkey_1 = self.vkeys_1[y]
            vkey_2 = self.vkeys_2[y]
            key2 = self.org_key2
            key3 = self.org_key3
            key4 = self.org_key4
            key2 = key2 + vkey_1
            key3 = key3 + vkey_1
            key4 = key4 - vkey_2
            j = y + 1
            going_to_salt = message[y*10:j*10]
            salted_message = self.add_salt(going_to_salt, key2, key3, key4)
            going_to_salt = salted_message
            salted_message = self.add_salt(going_to_salt,key2+1,key3+1,key4+1)
            random.seed(self.key1)
            encoded = 0
            encode_times = random.randint(key2, key3)
            while encoded != encode_times:
                random.seed(key2*key4)
                encoded_message = self.encode(salted_message)
                salted_message = encoded_message
                key2 = key2 +1
                key4 = key4 + 1
                encoded = encoded + 1
            key2 = self.org_key2 + vkey_1
            key4 = self.org_key4-vkey_2
            encrypted_message_list = []
            for char in encoded_message:
                encrypted_message_list.append(char)
            random.seed(key3*key4-key2)
            added_lenght = random.randint(0,self.key5)
            for x in range(0,added_lenght):
                encrypted_message_list.insert(random.randint(0,len(encrypted_message_list)),secrets.choice(self.outputs))
            encoded_message = ''.join(encrypted_message_list)
            chunck_list.append(encoded_message)
        f= open("swenigma_process_encryption_"+str(multiprocessing.current_process().name)+"_output_"+str(instance)+".txt","w")
        f.write("".join(chunck_list))
        f.close()
        process_pid = os.getpid()
        print('done')
        os.kill(process_pid,signal.SIGTERM)

    def decrypt_function(self,keyset,message):
        self.key1 = keyset[0]
        key2 = keyset[1]
        key3 = keyset[2]
        key4 = keyset[3]
        self.key5 = keyset[4]
        self.inputs = keyset[5]
        self.outputs = keyset[6]
        self.outputs_2 = keyset[7]
        self.outputs_3 = keyset[8]
        self.outputs_4 = keyset[9]
        self.chunks = 0
        self.vkeys_1 = []
        self.vkeys_2 = []
        self.message_list = []
        number_1_list = []
        number_1_lenght = 1
        for char in message:
            if char != '|':
                number_1_lenght = number_1_lenght + 1
                number_1_list.append(char)
            else:
                break
        number_1 = ''.join(number_1_list)
        number_1 = int(number_1)
        message = message[number_1_lenght:]
        number_2_list = []
        number_2_lenght = 1
        for char in message:
            if char != '|':
                number_2_lenght = number_2_lenght + 1
                number_2_list.append(char)
            else:
                break
        message = message[number_2_lenght:]
        number_2 = ''.join(number_2_list)
        number_2 = int(number_2)
        required_number_of_vkeys = (len(message) - len(message)%28)/28+1
        if number_2 != -1:
            random.seed(number_1+self.key1+key4)
            vkey_1_genetator = random.randint(key2,key3)
            random.seed(vkey_1_genetator)
            for i in range(0,int(required_number_of_vkeys)):
                self.vkeys_1.append(random.randint(round(key2/10),round(key2/2)))
            random.seed(number_2+self.key1+key4)
            vkey_2_genetator = random.randint(key2,key3)
            random.seed(vkey_2_genetator)
            for i in range(0,int(required_number_of_vkeys)):
                self.vkeys_2.append(random.randint(0+key2,2000+key2*key3*self.key1*key4))
        else:
            random.seed(number_1)
            vkey_1_genetator = random.randint(key2,key3)
            random.seed(vkey_1_genetator)
            for i in range(0,int(required_number_of_vkeys)):
                self.vkeys_1.append(random.randint(round(key2/10),round(key2/2)))
            vkey_2_genetator = random.randint(key2,key3)
            random.seed(vkey_2_genetator)
            for i in range(0,int(required_number_of_vkeys)):
                self.vkeys_2.append(random.randint(0+key2,2000+key2*key3*self.key1*key4))
        self.org_key4 = key4
        self.org_key2 = key2
        self.org_key3 = key3
        chunk_list = []
        chunk = 0
        while len(message) != 0:
            key3 = self.org_key3  
            key2 = self.org_key2
            key4 = self.org_key4
            vkey_1 = self.vkeys_1[chunk]
            vkey_2 = self.vkeys_2[chunk]
            key2 = key2 + int(vkey_1)
            key3 = key3 + int(vkey_1)
            key4 = key4 - int(vkey_2)
            random.seed(key3*key4-key2)
            number_of_false_chars = random.randint(0,self.key5)
            chunk_length = 28 + number_of_false_chars
            chunk_content = list(message[:chunk_length])
            false_chars_indexes = []
            for i in range(0,number_of_false_chars):
                false_chars_indexes.append(random.randint(0,len(chunk_content)-(number_of_false_chars-i)))
            for i in range(0,number_of_false_chars):
                chunk_content.pop(false_chars_indexes[len(false_chars_indexes)-i-1])
            chunk_list.append("".join(chunk_content))
            chunk = chunk +1
            message = message[chunk_length:]
        proc = []
        queues = []
        for i in range(0,self.processes):
            q = multiprocessing.Queue()
            queues.append(q)
            if i != self.processes -1:
                proc.append(multiprocessing.Process(target=self.core_decrypt_function, args=(chunk_list[int(math.ceil(i*len(chunk_list)/self.processes)):int(math.ceil((i+1)*len(chunk_list)/self.processes))],int(math.ceil(i*len(chunk_list)/self.processes)),q,),name=str(i)))
            else:
                proc.append(multiprocessing.Process(target=self.core_decrypt_function, args=(chunk_list[int(math.ceil(i*len(chunk_list)/self.processes)):int(math.ceil((i+1)*len(chunk_list)/self.processes))+1],int(math.ceil(i*len(chunk_list)/self.processes)),q,),name=str(i)))
        for p in proc:
            p.start() 
        for p in proc:
            p.join()
        for q in queues:
            que_content = q.get()
            self.message_list.append(que_content)
        x=  ''.join(self.message_list)
        return x
    def decode(self,message):
        result = ''
        for x in message:
            output = random.randint(1,4)
            if output == 1:
                index = self.outputs.index(x)
                result = result + self.inputs[index]
            if output == 2:
                index = self.outputs_2.index(x)
                result = result + self.inputs[index]
            if output == 3:
                index = self.outputs_3.index(x)
                result = result + self.inputs[index]
            if output == 4:
                index = self.outputs_4.index(x)
                result = result + self.inputs[index]
        return result
    def delete_salt(self,message,key2,key3,key4):
        desalting_complete = 0
        salting_table = []
        for x in message:
            salting_table.append(x)   
        keys = key3
        while desalting_complete != 2:
            random.seed(key4-keys-keys)
            salting_table.pop(random.randint(0, len(salting_table)-1))
            random.seed(key4*keys)
            salting_table.pop(random.randint(0, len(salting_table)-1))
            random.seed(key4+keys)
            salting_table.pop(random.randint(0, len(salting_table)-1))
            random.seed(key4-keys)
            salting_table.pop(random.randint(0, len(salting_table)-1))
            keys= key2
            desalting_complete = desalting_complete + 1
        random.seed(key4)
        salting_table.pop(random.randint(0, len(salting_table)-1))
        return ''.join(salting_table)
    
    def core_decrypt_function(self,recived_chunks,start_chunk_index,q):
        chunk_index = start_chunk_index
        decrypted_chunks_list = []
        for chunk in recived_chunks:
            key3 = self.org_key3  
            key2 = self.org_key2
            key4 = self.org_key4
            vkey_1 = self.vkeys_1[chunk_index]
            vkey_2 = self.vkeys_2[chunk_index]
            key2 = key2 + int(vkey_1)
            key3 = key3 + int(vkey_1)
            key4 = key4 - int(vkey_2)
            goingtodecode = chunk
            random.seed(self.key1)
            decoded = 0
            decode_times = random.randint(key2,key3)
            key2 = key2 + decode_times -1
            key4 = key4 + decode_times -1
            while decoded != decode_times:
                random.seed(key2*key4)
                decoded_message = self.decode(goingtodecode)
                goingtodecode= decoded_message
                key2 = key2 -1
                key4 = key4 -1
                decoded = decoded + 1
            key2 = self.org_key2 + vkey_1
            key4 = self.org_key4-vkey_2
            desalted_message = self.delete_salt(decoded_message, key2+1, key3+1, key4+1)
            goingtodesalt = desalted_message
            desalted_message = self.delete_salt(goingtodesalt,key2,key3,key4)
            decrypted_chunks_list.append(desalted_message)
            chunk_index = chunk_index +1
        q.put("".join(decrypted_chunks_list))
        print('done')
    #cryption functions
    #tested
    def encrypt(self,message,keyset_id='default_keyset',option ='ST',time_precsion = 0):
        if keyset_id == 'default_keyset':
            try:
                keyset= self.default_keyset
                encrypted_message = self.encrypt_function(keyset,message,option,time_precsion)
            except Exception as e:
                if self.fail_safe_status == 'on':
                    self.fail_safe(e)
        else:
            try:
                keyset = self.keysets[keyset_id]
                print(keyset)
                encrypted_message = self.encrypt_function(keyset,message,option,time_precsion)
            except Exception as e:
                print(e)
                print('The cause of the error is probably that you gave a keyset id that dose not exist')
                if self.fail_safe_status == 'on':
                    self.fail_safe(f"{e} The cause of the error is probably that you gave a keyset id that dose not exist")
        return encrypted_message
    #tested
    def decrypt(self,message,keyset_id='default_keyset',option = 'ST',time_precision = 0):
        if keyset_id == 'default_keyset':
            try:
                keyset = self.default_keyset
                decrypted_message = self.decrypt_function(keyset,message)
            except Exception as e:
                if self.fail_safe_status == 'on':
                    self.fail_safe(e)
        else:
            try:
                keyset = self.keysets[keyset_id]
                decrypted_message = self.decrypt_function(keyset,message)
            except Exception as e:
                print(e)
                print('The cause of the error is probably that you gave a keyset id that dose not exist')
                if self.fail_safe_status == 'on':
                    self.fail_safe(f"{e} The cause of the error is probably that you gave a keyset id that dose not exist")
        return decrypted_message
    #tested
    def encrypt_file(self,file_location,keyset_id='default_keyset',action='save',option = 'ST',time_precision = 0):
        try:
            f = open(file_location,'r')
            content = f.readlines(0)
            message = ''.join(content)
            f.close()
        except Exception as e:
            print(e)
            print(f"{file_location} file dose not exist")
            if self.fail_safe_status == 'on':
                self.fail_safe(f"{e} {file_location} file probably dose not exist")
        if keyset_id == 'default_keyset':
            try:
                keyset = self.default_keyset
                encrypted_message = self.encrypt_function(keyset,message,option,time_precsion=time_precision)
            except Exception as e:
                if self.fail_safe_status == 'on':
                    self.fail_safe(e)
        else:
            try:
                keyset = self.keysets[keyset_id]
                encrypted_message = self.encrypt_function(keyset,message,option,time_precision)
            except Exception as e:
                print(e)
                print('The cause of the error is probably that you gave a keyset id that dose not exist')
                if self.fail_safe_status == 'on':
                    self.fail_safe(f"{e} The cause of the error is probably that you gave a keyset id that dose not exist")
        if action=='save':
            print(encrypted_message)
            try:
                f = open(file_location,'w')
                f.write(encrypted_message)
                f.close()
            except Exception as e:
                print(e)
                print('you do not have premission to edit this file')
                print(f"encrypted file: {encrypted_message}")
                if self.fail_safe_status == 'on':
                    self.fail_safe(str(e)+' error saving file: '+str(file_location)+' after encrypting it.')
            return 
        elif action =='return':
            return encrypted_message
    #tested
    def decrypt_file(self,file_location,keyset_id='default_keyset',action='save',option = 'ST',time_precision = 0):
        try:
            f = open(file_location,'r')
        except:
            print(f"{file_location} file dose not exist")
        content = f.readlines(0)
        message = ''.join(content)
        f.close()
        if keyset_id == 'default_keyset':
            keyset = self.default_keyset
            decrypted_message = self.decrypt_function(keyset,message)
        else:
            try:
                keyset = self.keysets[keyset_id]
                decrypted_message = self.decrypt_function(keyset,message)
            except Exception as e:
                print(e)
                print('The cause of the error is probably that you gave a keyset id that dose not exist')
                if self.fail_safe_status == 'on':
                    self.fail_safe(f"{e} The cause of the error is probably that you gave a keyset id that dose not exist")
        if action=='save':
            try:
                f = open(file_location,'w')
                f.write(decrypted_message)
                f.close()
            except Exception as e:
                print('you do not have premission to edit this file')
                print(f"decrypted file: {decrypted_message}")
                if self.fail_safe_status == 'on':
                    self.fail_safe(str(e)+' error saving file: '+str(file_location)+' after decrypting it.')
            return
        elif action =='return':
            return decrypted_message
    #tested
    def shuffle_outputs(self,input_=['0'],seed=-1):
        input_ = list(input_)
        try:
            outputs = []
            if seed != -1:
                random.seed(seed)
            else:
                random.seed(time.time())
            
            random.shuffle(input_)
            outputs.append(input_[:])

            for i in range(4):
                random.shuffle(input_)
                outputs.append(input_[:])

        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e) + ' while trying to shuffle outputs')

        return outputs
    #keyset functions
    #tested
    def create_keyset(self,keyset_id,key1,key2,key3,key4,key5,inputs,outputs,outputs_2,outputs_3,outputs_4):
        try:
            if len(inputs)==len(outputs) and len(outputs)==len(outputs_2) and len(outputs_2)==len(outputs_3) and len(outputs_3)==len(outputs_4):
                keyset=[]
                keyset.append(key1)
                keyset.append(key2)
                keyset.append(key3)
                keyset.append(key4)
                keyset.append(key5)
                keyset.append(inputs)
                keyset.append(outputs)
                keyset.append(outputs_2)
                keyset.append(outputs_3)
                keyset.append(outputs_4)
                self.keysets[keyset_id]=keyset
            else:
                print('all outputs and the inputs are not the same lenght')
                if self.fail_safe_status == 'on':
                    self.fail_safe('outputs and inputs not the same lenght')
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to create keyset')
    #tested
    def save_keysets(self,file_location,keyset_ids=-1):
        try:
            if keyset_ids != -1:
                for id in keyset_ids:
                    selected_keysets  = {}
                    selected_keysets[id] = self.keysets[id]
            else:
                selected_keysets = self.keysets
            with open(f"{file_location}.json","w") as keysets_file:
                json.dump(selected_keysets,keysets_file)
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to save keysets')
    #tested
    def load_keysets(self,file_location):
        try:
            f = open(f"{file_location}.json")
            loaded_keysets = json.load(f)
            self.keysets.update(loaded_keysets)
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to load keysets')
    #tested
    def edit_keyset(self,keyset_id,new_keyset):
        try:
            self.keysets[keyset_id] = new_keyset
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to edit keysets')
    def delete_keyset(self,keyset_id):
        try:
            self.keysets.pop(keyset_id)
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to delete keysets')
    #tested
    def change_default_keyset(self,new_default_keyset):
        try:
            self.default_keyset = new_default_keyset
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to change default keyset')
    #tested
    def get_default_keyset(self):
        try:
            return self.default_keyset
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to get default keyset')
    #tested
    def get_keysets(self):
        try:
            return self.keysets
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to get keysets')
    def delete_saved_keysets(self,file_location):
        try:
            os.remove(f"{file_location}.json")
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to delete saved keysets')
    def change_number_of_processes(self,new_number):
        try:
            if isinstance(new_number,int) == True:
                self.processes = new_number
            else:
                if self.fail_safe_status == 'on':
                    self.fail_safe('you got caught trying to set the number of process to something else then a int')
        except Exception as e:
            if self.fail_safe_status == 'on':
                self.fail_safe(str(e)+' while trying to change number of processes')

