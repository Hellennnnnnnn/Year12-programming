import flet as ft
import datetime
import calendar
import os
import webbrowser
class CalendarApp:
    def __init__(self, page: ft.Page, events):
        self.page = page
        self.page.title = "Calendar"
        #self.page.window.width = page.width
        #self.page.window.height = page.height
        self.page.window.resizable = True
        self.current_date = datetime.datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month
        self.events = events  # Use the passed `events` dictionary instead of a local one

        self.create_widgets()
        self.update_calendar_days()
        self.update_time_and_date()

        self.page.on_resize = self.on_resize

    def create_widgets(self):
        self.top_frame = ft.Row(
            [
                ft.Text(value="", ref=ft.Ref(), style="headlineSmall", expand=True),
                ft.Text(value="", ref=ft.Ref(), style="headlineSmall", expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        self.date_label, self.time_label = self.top_frame.controls
        self.page.add(self.top_frame)

        self.header_frame = ft.Row(
            [
                ft.Dropdown(
                    options=[ft.dropdown.Option(str(i)) for i in range(1, 13)],
                    width=100,
                    value=str(self.month),
                    on_change=self.on_month_change
                ),
                ft.Dropdown(
                    options=[ft.dropdown.Option(str(i)) for i in range(1900, 2101)],
                    width=100,
                    value=str(self.year),
                    on_change=self.on_year_change
                ),
                ft.ElevatedButton(text="Today", on_click=self.go_to_today),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        self.page.add(self.header_frame)

        self.spacing_frame = ft.Container(
            height=20
        )
        self.page.add(self.spacing_frame)

        self.calendar_frame = ft.Column(
            spacing=2,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            auto_scroll=True
        )
        self.page.add(self.calendar_frame)

        # Add a button to create events
        self.add_event_button = ft.ElevatedButton(text="Add Event", on_click=self.open_event_dialog)
        self.page.add(self.add_event_button)

    def open_event_dialog(self, e):
        # Create a dialog to add an event with a description
        self.event_dialog = ft.AlertDialog(
            title=ft.Text("Add event"),
           content=ft.Column(
            [
                ft.TextField(label="Event Title", ref=ft.Ref()),
                ft.TextField(label="Date (YYYY-MM-DD)", ref=ft.Ref()),
               
                # Add a dropdown for selecting color
                ft.Dropdown(
                    label="Urgency Level",
                    options=[
                        ft.dropdown.Option("Very urgent"),
                        ft.dropdown.Option("Moderate"),
                        ft.dropdown.Option("Not urgent")
                    ],
                    ref=ft.Ref()  # Reference to capture user selection
                )
            ],
            spacing=10
        ),
            actions=[
                ft.TextButton("Add", on_click=self.add_event),
                ft.TextButton("Cancel", on_click=self.close_event_dialog)  # Close with cancel button
            ]
        )
        # Capture the event title, date, and description input references
        self.event_title_input, self.event_date_input, self.event_color_input = self.event_dialog.content.controls
        self.page.dialog = self.event_dialog
        self.event_dialog.open = True
        self.page.update()

    def add_event(self, e):
        event_title = self.event_title_input.value.strip()
        event_date_str = self.event_date_input.value.strip()
        
        event_color = self.event_color_input.value.strip()  # Capture selected color

        try:
            event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%d").date()
            if event_date not in self.events:
                self.events[event_date] = []
            # Store the title, description, and color as a tuple
            self.events[event_date].append((event_title, event_color))
            self.update_calendar_days()
            self.close_event_dialog(None)  # Close after adding
        except ValueError:
            # Handle invalid date format
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid date format. Use YYYY-MM-DD."))
            self.page.snack_bar.open = True

        self.page.update()

    def close_event_dialog(self, e):
        # Close the event dialog by setting open to False
        self.event_dialog.open = False
        self.page.update()
    def update_calendar_days(self):
        self.calendar_frame.controls.clear()
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Header row for days of the week
        day_row = ft.Row(
            [ft.Text(day, text_align=ft.TextAlign.CENTER, style="headlineSmall", expand=True) for day in days_of_week],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2
        )
        self.calendar_frame.controls.append(day_row)

        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(self.year, self.month)
        today = self.current_date.day if self.year == self.current_date.year and self.month == self.current_date.month else None

        for week in month_days:
            week_row = []
            for day in week:
                day_str = str(day) if day != 0 else ""
                event_texts = []
                if day != 0:
                    event_date = datetime.date(self.year, self.month, day)
                    if event_date in self.events:
                        # Create a list of ft.Text objects for each event title and color
                        event_texts = [
                            ft.Text(
                                f"{i + 1}. {title}",
                                color=self.get_event_color(color),  # Set the text color based on the selected event color
                                weight="bold"
                            )
                            for i, (title, color) in enumerate(self.events[event_date])
                        ]

                container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(day_str, text_align=ft.TextAlign.CENTER, style="labelLarge", size=12)
                        ] + event_texts,  # Add event texts directly to the column
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    margin=2,
                    expand=True,
                    height=50,
                    width=50,
                    border=ft.BorderSide(1, ft.colors.BLACK),
                    border_radius=ft.BorderRadius(
                        top_left=2, top_right=2, bottom_left=2, bottom_right=2
                    ),
                    on_click=lambda e, day=day: self.open_event_dialog_for_day(day)
                )
                if day == today:
                    container.bgcolor = ft.colors.BLUE_50
                week_row.append(container)
            self.calendar_frame.controls.append(
                ft.Row(week_row, alignment=ft.MainAxisAlignment.CENTER, expand=True)
            )

        self.page.update()

    
            # Helper method to get color based on the selected option
    def get_event_color(self, color):
        if color == "Very urgent":
            return ft.colors.RED
        elif color == "Moderate":
            return ft.colors.ORANGE
        elif color == "Not urgent":
            return ft.colors.GREEN
        return ft.colors.BLACK  # Default color if no match
    def open_event_dialog_for_day(self, day):
        if day != 0:
            self.event_date_input.value = f"{self.year}-{self.month:02}-{day:02}"
            self.show_events_for_day(day)

    def show_events_for_day(self, day):
        event_date = datetime.date(self.year, self.month, day)
        if event_date in self.events:
            # Show a dialog with all events for the day
            event_list = "\n".join([f"{i + 1}. {title}: {description}" for i, (title, description) in enumerate(self.events[event_date])])
            self.page.dialog = ft.AlertDialog(
                title=ft.Text(f"Events for {event_date}"),
                content=ft.Text(event_list),
            )
            self.page.dialog.open = True
            self.page.update()


    def update_time_and_date(self):
        now = datetime.datetime.now()
        self.time_label.value = now.strftime("%H:%M:%S")
        self.date_label.value = now.strftime("%Y-%m-%d")
        self.page.update()

    def go_to_today(self, e):
        self.current_date = datetime.datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month
        self.header_frame.controls[0].value = str(self.month)
        self.header_frame.controls[1].value = str(self.year)
        self.update_calendar_days()
        self.update_time_and_date()

    def on_month_change(self, e):
        self.update_calendar()

    def on_year_change(self, e):
        self.update_calendar()

    def on_resize(self, e):
        self.update_calendar_days()

    def update_calendar(self):
        self.year = int(self.header_frame.controls[1].value)
        self.month = int(self.header_frame.controls[0].value)
        self.update_calendar_days()
