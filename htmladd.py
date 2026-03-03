import csv

# Your HTML template with placeholders in curly braces
template = """<a href="{linkedin}" target="_blank" class="group text-center block hover:no-underline">
    <div class="profile-img-container w-24 h-24 mx-auto rounded-full bg-slate-200 mb-4 shadow-md border-2 border-white relative">
        <div class="absolute inset-0 bg-blue-600/50 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300">
            <i class="fa-brands fa-linkedin-in text-white text-xl"></i>
        </div>
        <img src="{image}" alt="{name}" class="w-full h-full object-cover rounded-full">
    </div>
    <h4 class="font-bold text-slate-900 text-sm group-hover:text-blue-600 transition">{name}</h4>
    <p class="text-xs text-blue-500 font-semibold mt-1">{topic}</p>
</a>
"""

# Open your CSV and create a new text file for the output
with open('delegates.csv', mode='r', encoding='latin-1') as csv_file, \
     open('output_html.txt', mode='w', encoding='utf-8') as txt_file:
    
    reader = csv.DictReader(csv_file)
    
    for row in reader:
        # Match these exact column names to the headers in your Google Sheet
        completed_html = template.format(
            linkedin=row['LinkedIn'],
            image=row['Image'],
            name=row['Name'],
            topic=row['Topic']
        )
        
        # Write to the text file and add a blank line between blocks
        txt_file.write(completed_html + "\n\n")

print("All done! Check the output_html.txt file.")