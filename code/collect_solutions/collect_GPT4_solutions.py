import pandas as pd
from progressive_data_collection import chat_with_gpt



if __name__ == "__main__":
	#load problems
	database_filename = 'database.xlsx' #the file that contains the problems
	sheet_name = 'Sheet1'
	xl = pd.ExcelFile(database_filename)
	df_problems = xl.parse(sheet_name) 

	#new dataframe to store solutions
	column_heads = ['ID','iter3', 'tag', 'solution_iter3','model']
	df_solutions = pd.DataFrame(columns=column_heads)
	write_filename = 'solutions.xlsx'
	
	#collecting non-forced solutions
	for  _,row in df_problems.iterrows():
    
        instruction_vanilla = f'Give a valid (feasible and efficient) solution very concisely. Use step1, step2, etc, and mention the tools to achieve each step. Use as few steps as possible and the answer should ideally be less than 100 words. When there is not a feasible solution given the constraint and provided tools, just say that it is not possible and give a very short justification.'

        index = row['ID']
        problem3 = row['iter3']
        text = f"{problem3}\n\n{instruction_vanilla}"
        conversation = [
                ("user", text),
            ]
        response3_vanilla = chat_with_gpt(conversation, T=1.0, max_tokens=800).replace('\n\n','\n').replace('\n','<br>\n')
        print(index, response3_vanilla, sep='\t')

        new_line = [index, row['iter3'], row['tag'], response3_vanilla,f"gpt4"]
        df_solutions.loc[len(df_solutions)] = new_line
        with pd.ExcelWriter(write_filename, mode='a', if_sheet_exists='overlay') as writer:  
            df_solutions.to_excel(writer, sheet_name=sheet_name, index=False)