from typing import List, Optional, Union

import typer
from rich import pretty
from rich.console import Console
from rich.table import Table

from database import complete_todo, delete_todo, get_all_todos, insert_todo, update_todo
from model import Todo

pretty.install()
console = Console()

app = typer.Typer()


@app.command(short_help="adds an item")
def add(task: str, category: str):
    # check if same task name exists
    init_msg = f"Trying to add task: {task} to category: {category}"
    todos = get_all_todos()
    for todo in todos:
        if todo.task == task:
            resp = f"A Task called {task} already exists. Try again with a different name."
            msg = fmt_response(init_msg, resp)
            show(msg)
            return
    todo = Todo(task, category)
    insert_todo(todo)
    resp = f'Success! Added "{task}" to "{category}"'
    msg = fmt_response(init_msg, resp)
    show(msg)


def fmt_response(init_msg: str, resp: str):
    initial_msg = typer.style(init_msg, fg=typer.colors.BRIGHT_YELLOW)
    if "Success" in resp:
        msg = initial_msg + typer.style("\n") + typer.style(resp, fg=typer.colors.BRIGHT_GREEN, bold=True)
    else:
        msg = initial_msg + typer.style("\n") + typer.style(resp, fg=typer.colors.BRIGHT_RED, bold=True)
    return msg


@app.command(short_help="deletes an item")
def delete(position: int):
    # indices in UI begin at 1, but in database at 0
    init_msg = f"Trying to delete task in position {position}..."
    response = delete_todo(position)
    msg = fmt_response(init_msg, response)
    show(msg)


@app.command(short_help="modifies existing task")
def update(position: int, task: Optional[str] = None, category: Optional[str] = None):
    init_msg = f"Trying to update {position}..."
    resp = update_todo(position - 1, task, category)
    msg = fmt_response(init_msg, resp)
    show(msg)


@app.command(short_help="mark an item as complete")
def complete(position: int):
    init_msg = f"Trying to mark {position} complete..."
    resp = complete_todo(position - 1)
    msg = fmt_response(init_msg, resp)
    show(msg)


@app.command(short_help="show all items in todo list")
def show(summary: Optional[str] = None):
    tasks = get_all_todos()
    console.clear()
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    table = _show_tasks(tasks, table)
    # for idx, task in enumerate(tasks, start=1):
    #    c = get_category_color(task.category)
    #    is_done_str = '✅' if task.status == 2 else '❌'
    #    table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', is_done_str)
    console.print(table)
    if summary:
        summary_msg = typer.style("Summary:", fg=typer.colors.GREEN, bold=True, underline=True)
        typer.echo(summary_msg)
        typer.echo(f"{summary}")


def _show_tasks(tasks: List[Todo], table: Table, selected_tasks: Union[List, None] = None):
    if isinstance(_show_tasks, str):
        selected_tasks = [selected_tasks]
    if selected_tasks is None and tasks is not None:
        selected_tasks = tasks

    # filter tasks
    for idx, task in enumerate(tasks):
        if task.task in selected_tasks[idx].task:
            c = get_category_color(task.category)
            is_done_str = "✅" if task.status == 2 else "❌"
            table.add_row(str(idx), task.task, f"[{c}]{task.category}[/{c}]", is_done_str)
        else:
            pass
    return table


def get_category_color(category):
    COLORS = {"Learn": "cyan", "Personal Errands": "red", "Fun": "cyan", "Study": "green"}
    if category in COLORS:
        return COLORS[category]
    return "white"


if __name__ == "__main__":
    app()
