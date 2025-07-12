import ui
import json
import os
import webbrowser
import objc_util

DATA_FILE = 'channels.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def open_in_safari(url):
    from objc_util import ObjCClass, nsurl
    UIApplication = ObjCClass('UIApplication')
    NSURL = nsurl(url)
    app = UIApplication.sharedApplication()
    app.openURL_(NSURL)


class EditForm(ui.View):
    def __init__(self, title='', url='', category='', disabled=False, on_save=None):
        self.name = 'Edit Channel'
        self.background_color = 'white'
        self.frame = (0, 0, 360, 280)
        self.on_save = on_save

        self.title_field = ui.TextField(frame=(20, 30, 320, 32), text=title, placeholder='Title')
        self.url_field = ui.TextField(frame=(20, 80, 320, 32), text=url, placeholder='URL')
        self.category_field = ui.TextField(frame=(20, 130, 320, 32), text=category, placeholder='Category')

        self.disabled_switch = ui.Switch(frame=(20, 180, 100, 32))
        self.disabled_switch.value = disabled
        self.disabled_label = ui.Label(frame=(80, 180, 200, 32), text='Disabled', font=('Helvetica', 14))

        self.save_btn = ui.Button(title='Save', frame=(20, 230, 150, 32), action=self.save)
        self.cancel_btn = ui.Button(title='Cancel', frame=(190, 230, 150, 32), action=self.close)

        for view in [
            self.title_field, self.url_field, self.category_field,
            self.disabled_switch, self.disabled_label,
            self.save_btn, self.cancel_btn
        ]:
            self.add_subview(view)

    def save(self, sender):
        title = self.title_field.text.strip()
        url = self.url_field.text.strip()
        category = self.category_field.text.strip()
        disabled = self.disabled_switch.value
        if title and category and self.on_save:
            self.on_save(title, url, category, disabled)
        self.close()

    def close(self, sender=None):
        super().close()


class LinkBrowser(ui.View):
    def __init__(self):
        self.name = 'Channel List'
        self.flex = 'WH'
        self.background_color = 'white'

        self.data = load_data()
        self.filtered_data = self.data.copy()
        self.grouped = self.group_and_sort(self.filtered_data)

        self.searchbar = ui.TextField(placeholder='Search', flex='W', height=32)
        self.searchbar.action = self.search_action

        self.new_button = ui.Button(title='New', frame=(self.width - 70, 0, 70, 32), action=self.new_item)
        self.new_button.flex = 'L'

        self.table = ui.TableView(flex='WH')
        self.table.delegate = self
        self.table.data_source = self

        self.add_subview(self.searchbar)
        self.add_subview(self.new_button)
        self.add_subview(self.table)

        self.searchbar.frame = (0, 0, self.width - 70, 32)
        self.table.frame = (0, 32, self.width, self.height - 32)
        self.autoresizing = 'WH'

    def search_action(self, sender):
        term = sender.text.lower()
        self.filtered_data = {
            k: [item for item in v if term in item['title'].lower()]
            for k, v in self.data.items()
        }
        self.grouped = self.group_and_sort(self.filtered_data)
        self.table.reload()

    def group_and_sort(self, data):
        return {
            k: sorted(v, key=lambda x: x['title'])
            for k, v in sorted(data.items())
        }

    def tableview_number_of_sections(self, tableview):
        return len(self.grouped)

    def tableview_number_of_rows(self, tableview, section):
        return len(list(self.grouped.values())[section])

    def tableview_title_for_header(self, tableview, section):
        return list(self.grouped.keys())[section]

    def tableview_cell_for_row(self, tableview, section, row):
        category = list(self.grouped.keys())[section]
        item = self.grouped[category][row]
        cell = ui.TableViewCell()
        cell.text_label.text = item['title']
        if item.get('disabled', False) or not item.get('url'):
            cell.text_label.text_color = 'gray'
        return cell

    def tableview_did_select(self, tableview, section, row):
        def show_actions():
            category = list(self.grouped.keys())[section]
            item = self.grouped[category][row]

            options = [item['url']]
            if item.get('url') and not item.get('disabled', False):
                options.append('Open in Safari')
            options.extend(['Edit', 'Delete'])

            try:
                import console
                choice = console.alert(item['title'], *options)
                action = options[choice]
                if action == 'Open in Safari':
                    open_in_safari(item['url'])
                elif action == 'Edit':
                    self.edit_item(category, row)
                elif action == 'Delete':
                    self.remove_item(category, row)
            except Exception:
                pass

        ui.delay(show_actions, 0.1)

    def edit_item(self, category, row):
        original_item = self.grouped[category][row]

        def save_edit(new_title, new_url, new_category, disabled):
            for item in self.data[category]:
                if item['title'] == original_item['title'] and item.get('url', '') == original_item.get('url', ''):
                    self.data[category].remove(item)
                    break
            if not self.data[category]:
                del self.data[category]

            self.data.setdefault(new_category, []).append({
                'title': new_title,
                'url': new_url,
                'disabled': disabled
            })
            save_data(self.data)
            self.filtered_data = self.data.copy()
            self.grouped = self.group_and_sort(self.filtered_data)
            self.table.reload()

        form = EditForm(
            title=original_item['title'],
            url=original_item.get('url', ''),
            category=category,
            disabled=original_item.get('disabled', False),
            on_save=save_edit
        )
        form.present('sheet')

    def remove_item(self, category, row):
        item_to_remove = self.grouped[category][row]
        self.data[category].remove(item_to_remove)
        if not self.data[category]:
            del self.data[category]
        save_data(self.data)
        self.filtered_data = self.data.copy()
        self.grouped = self.group_and_sort(self.filtered_data)
        self.table.reload()

    def new_item(self, sender):
        def save_new(title, url, category, disabled):
            self.data.setdefault(category, []).append({
                'title': title,
                'url': url,
                'disabled': disabled
            })
            save_data(self.data)
            self.filtered_data = self.data.copy()
            self.grouped = self.group_and_sort(self.filtered_data)
            self.table.reload()

        form = EditForm(on_save=save_new)
        form.present('sheet')


# Run the app
view = LinkBrowser()
view.present('sheet')
