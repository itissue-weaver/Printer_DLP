# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 20/feb/2025  at 14:21 $"

import json
from tkinter import messagebox

import ttkbootstrap as ttk
from PIL import Image, ImageTk

from files.constants import font_buttons, font_title, path_no_image, path_solid_capture, desired_width_thumbnail
from templates.AuxiliarFunctions import (
    read_projects,
    update_settings,
    create_new_project,
    delete_project,
)


class HomePage(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.current_data_p = None
        self.frame_new_project = None
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        self.callbacks = kwargs.get("callbacks")
        # ------------------------ProjectFilesSelector----------------------
        self.frame_new = ttk.Frame(self)
        self.frame_new.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.frame_new.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_new,
            text="New Project",
            command=self.new_project_callback,
            style="success.TButton",
        ).grid(row=0, column=0, padx=10, pady=10)

        self.frame_previous = ttk.Frame(self)
        self.frame_previous.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.frame_previous.columnconfigure(0, weight=1)
        projects = read_projects()
        data_lists = [
            [
                k,
                v.get("name"),
                v.get("timestamp"),
                v.get("user"),
                v.get("status"),
                json.dumps(v),
            ]
            for k, v in projects.items()
        ]
        data_lists.sort(key=lambda x: x[2], reverse=True)
        self.current_project_key = data_lists[0][0]
        self.current_p_text = ttk.StringVar(
            value=f"Current Project: {data_lists[0][1]}"
        )
        ttk.Label(
            self.frame_previous,
            textvariable=self.current_p_text,
            font=font_buttons,
            style="Custom.TLabel",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ttk.Label(
            self.frame_previous,
            text="Previous Projects",
            font=font_buttons,
            style="Custom.TLabel",
        ).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.tv_projects = ttk.Treeview(
            self.frame_previous,
            columns=(
                "key",
                "name",
                "Last modified",
                "User",
                "Status",
                "data",
                "action",
            ),
            show="headings",
            style="Custom.Treeview",
        )
        self.tv_projects.grid(row=2, column=0, padx=10, pady=10)
        self.tv_projects.configure(
            columns=("key", "name", "Last modified", "User", "Status", "data", "action")
        )
        for col in self.tv_projects["columns"]:
            self.tv_projects.heading(col, text=col.title(), anchor="w")
        self.tv_projects.configure(
            columns=("key", "name", "Last modified", "User", "Status", "data", "action")
        )

        for col in self.tv_projects["columns"]:
            self.tv_projects.heading(col, text=col.title(), anchor="n")
            if col == "name":
                self.tv_projects.column(col, stretch=True, width=150)
            elif col == "Last modified":
                self.tv_projects.column(col, stretch=False, width=250)
            elif col == "User":
                self.tv_projects.column(col, stretch=False, width=100)
            elif col == "Status":
                self.tv_projects.column(col, stretch=False, width=120)
            elif col == "data":
                self.tv_projects.column(col, stretch=False, width=0)  # Ocultar columna
            elif col == "key":
                self.tv_projects.column(col, stretch=False, width=0)  # Ocultar columna
            elif col == "action":
                self.tv_projects.column(
                    col, stretch=False, width=120
                )  # Ocultar columna
        # insert data
        for item in data_lists:
            self.tv_projects.insert("", "end", values=item + ["Delete"])
        self.tv_projects.bind("<Double-1>", self.item_selected_treeview)
        self.frame_thumbnails = ttk.Frame(self)
        self.frame_thumbnails.grid(
            row=0, column=2, columnspan=2, sticky="ew", padx=10, pady=10
        )
        self.frame_thumbnails.columnconfigure(0, weight=1)
        self.render_thumbnails(path_solid_capture)

    def render_thumbnails(self, filepath):
        for child in self.frame_thumbnails.winfo_children():
            child.destroy()
        try:
            image_thumbnail = Image.open(filepath)
        except FileNotFoundError:
            image_thumbnail = Image.open(path_no_image)
        width, height = image_thumbnail.size
        factor = desired_width_thumbnail / width
        new_height = int(height * factor)
        image_thumbnail = image_thumbnail.resize((desired_width_thumbnail, new_height))
        background_image = ImageTk.PhotoImage(image_thumbnail)
        canvas_thumbnail = ttk.Canvas(
            self.frame_thumbnails,
            width=background_image.width(),
            height=background_image.height(),
        )
        canvas_thumbnail.grid(row=0, column=0, padx=10, pady=10)
        canvas_thumbnail.create_image(0, 0, anchor="nw", image=background_image)
        canvas_thumbnail.image = background_image

    def new_project_callback(self):
        if self.frame_new_project is None:
            callback = {"reload_treeview": self.reload_treeview}
            self.frame_new_project = NewProjectWindow(self, callbacks=callback)

    def reload_treeview(self):
        projects = read_projects()
        data_lists = [
            [
                k,
                v.get("name"),
                v.get("timestamp"),
                v.get("user"),
                v.get("status"),
                json.dumps(v),
            ]
            for k, v in projects.items()
        ]
        data_lists.sort(key=lambda x: x[2], reverse=True)
        self.tv_projects.delete(*self.tv_projects.get_children())
        for item in data_lists:
            self.tv_projects.insert("", "end", values=item + ["Delete"])
        self.tv_projects.bind("<Double-1>", self.item_selected_treeview)
        self.callbacks["change_project"](self.current_project_key)


    def item_selected_treeview(self, event):
        values = event.widget.item(event.widget.selection()[0], "values")[:-1]
        column = event.widget.identify_column(event.x)
        column_index = int(column[1:]) - 1
        if column_index == 6:
            msg = "Are you sure to delete this project?"
            answer = messagebox.askyesno("Delete Project", msg)
            if answer == "No":
                return
            delete_project(values[0])
            print("delete project", values[0])
            self.reload_treeview()
            return
        data = json.loads(values[-1])
        self.current_project_key = values[0]
        self.current_p_text.set(f"Current Project: {data.get('name')}")
        self.callbacks["change_title"](f"Project: {data.get('name')}")
        update_settings(**data.get("settings", {}))
        self.current_data_p = data
        self.callbacks["change_tab_text"](
            data.get("settings", {"status_frames"}).get("status_frames", [0, 0, 0, 0])
        )
        self.callbacks["init_tabs"]()
        self.callbacks["change_project"](self.current_project_key)
        self.render_thumbnails(path_solid_capture)


class NewProjectWindow(ttk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.master = master
        self.title("New Project")
        self.attributes("-topmost", True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame = NewProjectForm(self, **kwargs)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.frame.on_close(from_parent=True)
        self.destroy()


def create_widgets_form_new_project(master):
    ttk.Label(master, text="Project Data", font=font_title).grid(
        row=0, column=0, sticky="n", padx=10, pady=10
    )

    frame_widgets = ttk.Frame(master)
    frame_widgets.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_widgets.columnconfigure(0, weight=1)

    entries = []
    ttk.Label(frame_widgets, text="Project Name", style="Custom.TLabel").grid(
        row=0, column=0, sticky="n", padx=10, pady=10
    )
    entry_name = ttk.StringVar()
    ttk.Entry(frame_widgets, textvariable=entry_name, style="Custom.TEntry").grid(
        row=1, column=0, sticky="n", padx=10, pady=10
    )
    entries.append(entry_name)

    ttk.Label(frame_widgets, text="Project user", style="Custom.TLabel").grid(
        row=2, column=0, sticky="n", padx=10, pady=10
    )
    entry_user = ttk.StringVar()
    ttk.Entry(frame_widgets, textvariable=entry_user, style="Custom.TEntry").grid(
        row=3, column=0, sticky="n", padx=10, pady=10
    )
    entries.append(entry_user)

    return entries


class NewProjectForm(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.master = master
        self.callbacks = kwargs.get("callbacks")
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Project Data", font=font_title).grid(
            row=0, column=0, sticky="n", padx=10, pady=10
        )

        self.frame_widgets = ttk.Frame(self)
        self.frame_widgets.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.entries = create_widgets_form_new_project(self.frame_widgets)

        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_buttons.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Create",
            command=self.on_close,
            style="success.TButton",
        ).grid(row=0, column=0, sticky="e", padx=10, pady=10)

    def on_close(self, from_parent=False):
        data = [entry.get() for entry in self.entries]
        for item in data:
            if item == "":
                return
        create_new_project(
            {
                "name": data[0],
                "user": data[1],
                "thumbnail": "",
                "status": 0,
            }
        )
        self.callbacks["reload_treeview"]()
        print("create new project", data[0])
        if not from_parent:
            self.master.destroy()
