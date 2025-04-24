CONSIDRATIONS:
- what if i use forms directory to store each form in a text file individually.
does it make the updating easier.


QUESTIONS:
is it must tab oriented ?
if forms name wasn't unique and if user wants to edit a from 
and we able to show the forms for user after editing which form
will updated in the json file, first one, second one, or what
clearly we have develop a method to distinguesh between forms. eigter make
them unique with id field or make them unique in form name.

MAYBE: 
write some helper functions like is_empty
border style used two times 

[O] TODO: before save form check fields to not be empty
[O] TODO: Form name lineedit
TODO: Remove field
TODO: What if user wants to change order of fields(row) if missed columns order
TODO: I think I have to destroy fields after form been saved.

[O] TODO: Set focus to field name
check if last row not invalid

TODO: check form name not be empty
TODO: check at last one row with field name and type exist in the form layout^J

TODO: When you save a form in formbilder it must add to list of forms in formedit tab.

Maybe you should change File to something for Fome to form operation like get
form_names get_form_fields and etc which are common any most of the
FormSomthing classes ;

change field_type to field_types

display message on some situation like from saved edit something delete and etc

# TODO: User should be able to add new fields in edit form tab
# TODO: Create new tab using tab key.
# TODO: table data should act based on their type.

#TODO: multi choice should be in a seperate menu action and form.
# TODO: scroll for form create window
#TODO: close button for each field(row)

#TODO:
- Make english version of choices to work eaiser in programming side;
- Add message to status bar on save or when user make a misstake
- Create log file eventually.
- first field that designed in qt designer make some problem i could remove it
and create row field programactically when FormCreate appear

