import flet as ft
import os
import webbrowser
from calendar_widget_code import CalendarApp

def main(page: ft.Page):
    # App title
    page.title = "Deadline Dash"
    
    # Dictionary to store events across views
    events = {}

    # State variable to track the current view (True for calendar, False for To-Do List)
    is_calendar_view = False

    # Container for the To-Do List
    pagelet_container = ft.Container(
        width= page.width,
        height= page.height,
        content=ft.TextField(
            label="Click here to start typing",
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            multiline=True,
            border="None",
            bgcolor=ft.colors.CYAN_100,
            height=(4 / 6.5 * page.height),
            color= ft.colors.BLACK
        )
    )

    # Theme toggle function
    def toggle_theme(e):
        if theme_switch.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    # Function to create a new folder
    def create_folder(e):
        folder_name = folder_input.value.strip()
        if folder_name and folder_name not in folders:
            folders[folder_name] = []  # Initialize an empty list for the folder's files
            folder_list.controls.append(ft.TextButton(text=folder_name, on_click=open_folder))
            
            folder_input.value = ""
            page.update()

    # Function to open a folder
    def open_folder(e):
        selected_folder = e.control.text
        upload_panel.content.controls[0].value = f"Folder: {selected_folder}"
        upload_panel.data = selected_folder  # Store folder name in panel's data attribute
        upload_panel.visible = True
        sidebar_container.visible = False
        file_list.controls.clear()  # Clear the file list before adding new files
        for file_path in folders[selected_folder]:
            file_name = os.path.basename(file_path)
            file_list.controls.append(ft.TextButton(text=file_name, on_click=lambda e, p=file_path: open_file(p)))
        page.update()

    # Function to handle file upload
    def upload_files(e):
        selected_folder = upload_panel.data
        if selected_folder:
            for file in file_picker.result.files:
                file_path = file.path  # Store the full path of the file
                folders[selected_folder].append(file_path)
                file_name = os.path.basename(file_path)
                file_list.controls.append(ft.TextButton(text=file_name, on_click=lambda e, p=file_path: open_file(p)))
            page.update()

    # Function to open a file using the default application
    def open_file(file_path):
        webbrowser.open(file_path)

    # Function to go back to the folder list
    def back_to_folders(e):
        upload_panel.visible = False
        sidebar_container.visible = True
        page.update()

    # Show/hide settings container
    def theme_settings_container(e):
        settings_container.visible = not settings_container.visible
        page.update()

    # Show/hide the sidebar for adding folders
    def sidebar_panel(e):
        sidebar_container.visible = not sidebar_container.visible
        page.update()

    # Function to toggle between calendar and to-do list views
    def toggle_view(e):
        nonlocal is_calendar_view

        if is_calendar_view:
            # Show To-Do List view
            page.clean()
            #page.add(NavBar(toggle_view, sidebar_panel, theme_settings_container), settings_container, sidebar_container, upload_panel, pagelet_container)
            
            #creating calendar stored in a container
            
            #need to stack the elements between the switches so that the folders sidebar works
            page.add(
                ft.Stack(
                    [
                        
                        # Add the main page elements first
                        ft.Column(
                            [
                                NavBar(toggle_view, sidebar_panel, theme_settings_container),
                                settings_container,
                                #sidebar_container,
                                #upload_panel,
                                pagelet_container
                            ]
                        ),
                        # Add the sidebar container as an overlay
                        #NEED TO FIX STACKING FOR 2 ELEMENTS BELOW
                        ft.Column(
                            [
                                upload_panel,
                                sidebar_container
                            ]
                        )
                        
                        
                    ]
                )
    )

        else:
            # Show Calendar view
            page.clean()
            #page.add(NavBar(toggle_view, sidebar_panel, theme_settings_container), sidebar_container,upload_panel)
            #need to stack the elements between the switches so that the folders sidebar works
            
            page.add(
                ft.Stack(
                    [
                        
                        # Add the main page elements first
                        ft.Column(
                            [
                                NavBar(toggle_view, sidebar_panel, theme_settings_container),
                                #sidebar_container,
                                #upload_panel,
                                
                                
                            ]
                        ),
                        # Add the sidebar container as an overlay
                        #NEED TO FIX STACKING FOR 2 ELEMENTS BELOW
                        ft.Column(
                            [
                                upload_panel,
                                sidebar_container
                            ]
                        )
                        
                        
                    ]
                ))
    
            calendar_container = ft.Container(
                content = CalendarApp(page, events),  # Pass the events dictionary to CalendarApp
                width=800,
                height= page.height
            )

        is_calendar_view = not is_calendar_view  # Toggle the view state

    
    #image widget for app icon
    #usual height and width of an icon is 50px
    icon_widget = ft.Image(
        src="./deadline_dash_logo.png",
        width=50,
        height=50
    )
    icon_whole = ft.Container(
            content = icon_widget,
            #puts the icon in the center of the nav container on the left hand side
            alignment=ft.alignment.center_left,
            padding=10,
    )
    
    # Navbar component
    def NavBar(toggle_view_fn, sidebar_panel_fn, theme_settings_fn):
        return ft.Container(
            #width=page.width,
            height=page.height / 6,
            bgcolor=ft.colors.CYAN_400,
            border_radius=5,
            content=ft.Row(
                
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    icon_whole,
                    ft.Row(
                        controls=[
                            ft.Container(  
                        # App icon container
                        content=ft.Icon(name=ft.icons.CALENDAR_TODAY, color=ft.colors.WHITE, size=35),
                        padding=10,
                        #event caller to perform whats in the function
                        on_click=toggle_view_fn),
                                            
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(text="Add:"),
                                    ft.PopupMenuItem(icon=ft.icons.CREATE_NEW_FOLDER_ROUNDED, text="Assignment", on_click=sidebar_panel_fn),
                                ],
                                icon_color=ft.colors.WHITE,
                                icon=ft.icons.ADD_ROUNDED,
                                icon_size=40
                            ),
                            # Replace the settings cog with the theme switch
                            theme_switch
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
            ),
    )

    # Switch widget for theme toggle
    theme_switch = ft.Switch(
        value=False,
        on_change=toggle_theme
    )

    # Dark/light mode text
    theme_mode_text = ft.Text(
        value="Mode:",
        style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK54),
    )

    # Dictionary to store folder names and their associated files
    folders = {}

    # FilePicker for uploading files
    file_picker = ft.FilePicker(on_result=upload_files)
    page.overlay.append(file_picker)

    # Sidebar for folder creation and management
    folder_input = ft.TextField(label="Assignment name", width=200,color= ft.colors.BLACK,label_style=ft.TextStyle(color=ft.colors.BLACK),)
    folder_create_btn = ft.ElevatedButton(text="Create Folder", on_click=create_folder)
    folder_list = ft.Column()

    # Settings container
    settings_container = ft.Container(
        bgcolor=ft.colors.GREY_100,
        padding=ft.padding.only(30, 10, 0, 30),
        border_radius=5,
        width=page.width,
        height=page.height / 2,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.GREY,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        visible=False,
        content=ft.Column(
            [
                ft.Text(
                    value="Settings",
                    style=ft.TextStyle(size=25, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ),
                ft.Row(
                    controls=[
                        theme_mode_text,
                        theme_switch
                    ]
                )
            ]
        ),
    )

    # Sidebar container
    sidebar_container = ft.Container(
        bgcolor=ft.colors.GREY_300,
        #z_index=110,
        padding=ft.padding.only(50, 10, 0, 30),
        border_radius=5,
        width=page.width / 3,
        height=500,
        visible=False,
        #z_index=10,  # Ensures it's on top of other elements
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.GREY,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER),
        content=ft.Column(
            [
                ft.Text(
                    value="Folders:",
                    style=ft.TextStyle(size=25, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                    text_align=ft.TextAlign.CENTER
                ),
                folder_input,
                folder_create_btn,
                folder_list,
            ]
        )
    )

    # File list for uploaded files
    file_list = ft.Column()

    # Upload panel for file upload in a folder
    upload_panel = ft.Container(
        visible=False,
        #z_index=100,
        bgcolor=ft.colors.GREY_100,
        padding=ft.padding.only(30, 10, 0, 30),
        width= page.width/2,
        height= 400,
        border_radius=5,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.GREY,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        
        content=ft.Column(
            [
                ft.Text(value="Folder: ", style=ft.TextStyle(size=25, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)),
                ft.ElevatedButton("Upload from Device", on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
                file_list,
                ft.ElevatedButton("Back", on_click=back_to_folders)
            ]
        )
    )

    # Add components to the page
    #page.add(NavBar(toggle_view, sidebar_panel, theme_settings_container), settings_container, upload_panel, pagelet)
    #page.overlay.append(sidebar_container)
    # Use Stack to layer components
    page.add(
        ft.Stack(
            [
                
                # Add the main page elements first
                ft.Column(
                    [
                        NavBar(toggle_view, sidebar_panel, theme_settings_container),
                        settings_container,
                        pagelet_container
                    ]
                ),
                # Add the sidebar container as an overlay
                #NEED TO FIX STACKING FOR 2 ELEMENTS BELOW
                ft.Column(
                    [
                        upload_panel,
                        sidebar_container
                    ]
                )
                
                
            ]
        )
    )
    
    # Update page
    page.update()

# THIS LINE IS IMPORTANT!!! IT OPENS THE CODE IN A NEW WINDOW 
ft.app(target=main)
