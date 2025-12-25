import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np


class FeedRequirementCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет потребности в кормах")
        self.root.geometry("500x500")

        # Нормативы потребности на 1 голову в день (в ц)
        self.feed_norms = {
            'Концентраты': 5,
            'Сено': 15,
            'Силос': 20
        }

        # Данные за предыдущие годы (в ц)
        self.previous_years_data = {
            'Позапрошлый год': 51000,
            'Прошлый год': 29500
        }

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Расчет потребности в кормах",
            font=("Arial", 12, "bold")
        )
        title_label.pack(anchor='w', padx=20, pady=10)

        # Поголовье коров
        tk.Label(self.root, text="Поголовье коров, гол.:").pack(anchor='w', padx=20)
        self.herd_input = tk.Entry(self.root, width=30)
        self.herd_input.pack(anchor='w', padx=20, pady=5)

        # Количество дней содержания
        tk.Label(self.root, text="Количество дней содержания:").pack(anchor='w', padx=20)
        self.days_input = tk.Entry(self.root, width=30)
        self.days_input.pack(anchor='w', padx=20, pady=5)

        # Вид корма
        tk.Label(self.root, text="Вид корма:").pack(anchor='w', padx=20)

        self.feed_type_var = tk.StringVar(value='Концентраты')
        self.feed_type_combo = ttk.Combobox(
            self.root,
            textvariable=self.feed_type_var,
            values=list(self.feed_norms.keys()),
            state='readonly',
            width=30
        )
        self.feed_type_combo.pack(anchor='w', padx=20, pady=5)

        # Кнопка расчета потребности
        self.calculate_button = tk.Button(
            self.root,
            text="Рассчитать потребность",
            command=self.calculate_requirement,
            bg='lightblue'
        )
        self.calculate_button.pack(anchor='w', padx=20, pady=10)

        # Результат расчета потребности
        tk.Label(self.root, text="Потребность в кормах, ц:").pack(anchor='w', padx=20)
        self.result_entry = tk.Entry(self.root, width=30, state='readonly')
        self.result_entry.pack(anchor='w', padx=20, pady=5)

        # Кнопка построения графика
        self.graph_button = tk.Button(
            self.root,
            text="Построить график сравнения",
            command=self.show_comparison_chart,
            bg='lightgreen'
        )
        self.graph_button.pack(anchor='w', padx=20, pady=10)

        # Информация о нормативах
        self.create_norms_table()

    def create_norms_table(self):
        # Создаем фрейм для таблицы нормативов
        norms_frame = tk.LabelFrame(self.root, text="Нормативы потребности на 1 голову в день", padx=10, pady=10)
        norms_frame.pack(fill='x', padx=20, pady=10)

        # Заголовки таблицы
        headers = ['Вид корма', 'Потребность, ц']
        for col, header in enumerate(headers):
            tk.Label(norms_frame, text=header, font=("Arial", 9, "bold")).grid(row=0, column=col, padx=10, pady=5)

        # Данные таблицы
        for row, (feed_type, norm) in enumerate(self.feed_norms.items(), start=1):
            tk.Label(norms_frame, text=feed_type).grid(row=row, column=0, padx=10, pady=2, sticky='w')
            tk.Label(norms_frame, text=str(norm)).grid(row=row, column=1, padx=10, pady=2, sticky='e')

    def calculate_requirement(self):
        try:
            # Получаем данные из полей ввода
            herd_size = float(self.herd_input.get())
            days = float(self.days_input.get())
            feed_type = self.feed_type_var.get()

            # Проверка корректности данных
            if herd_size <= 0 or days <= 0:
                raise ValueError("Значения должны быть положительными числами")

            # Получаем норматив для выбранного корма
            norm = self.feed_norms.get(feed_type, 0)

            # Расчет потребности
            # Потребность = Поголовье коров * количество дней содержания * Норматив потребности на 1 голову
            requirement = herd_size * days * norm

            # Вывод результата
            self.result_entry.config(state='normal')
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, f"{requirement:.2f}")
            self.result_entry.config(state='readonly')

            # Показать информацию о расчете
            messagebox.showinfo(
                "Результат расчета",
                f"Потребность в корме '{feed_type}': {requirement:.2f} ц\n\n"
                f"Расчет: {herd_size} гол. × {days} дн. × {norm} ц/гол. = {requirement:.2f} ц"
            )

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Пожалуйста, введите корректные числовые значения.\nОшибка: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def show_comparison_chart(self):
        try:
            # Получаем текущую потребность
            result_text = self.result_entry.get()
            if not result_text:
                messagebox.showwarning("Нет данных", "Сначала выполните расчет потребности")
                return

            current_requirement = float(result_text)
            feed_type = self.feed_type_var.get()

            # Подготавливаем данные для графика
            years = ['Позапрошлый год', 'Прошлый год', 'Текущий расчет']
            requirements = [
                self.previous_years_data['Позапрошлый год'],
                self.previous_years_data['Прошлый год'],
                current_requirement
            ]

            # Создаем точечный график
            fig, ax = plt.subplots(figsize=(10, 6))

            # Создаем точки для каждого года
            x_positions = np.arange(len(years))

            # Рисуем точки
            scatter = ax.scatter(x_positions, requirements, s=200, alpha=0.7,
                                 c=['red', 'blue', 'green'], edgecolors='black', linewidth=2)

            # Добавляем соединительные линии (опционально)
            ax.plot(x_positions, requirements, 'k--', alpha=0.3, linewidth=1)

            # Добавляем подписи значений
            for i, (year, req) in enumerate(zip(years, requirements)):
                ax.annotate(f'{req:,.0f} ц',
                            xy=(i, req),
                            xytext=(0, 10),
                            textcoords='offset points',
                            ha='center',
                            fontsize=10,
                            fontweight='bold')

            # Настройки графика
            ax.set_title(f'Сравнение потребности в кормах ({feed_type})', fontsize=14, fontweight='bold')
            ax.set_xlabel('Период', fontsize=12)
            ax.set_ylabel('Потребность, ц', fontsize=12)
            ax.set_xticks(x_positions)
            ax.set_xticklabels(years, fontsize=11)

            # Добавляем сетку
            ax.grid(True, alpha=0.3, linestyle='--')

            # Добавляем легенду для цветов
            color_labels = ['51000 ц', '29500 ц', f'{current_requirement:.0f} ц']
            handles = [plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=color, markersize=10,
                                  markeredgecolor='black', linewidth=2)
                       for color in ['red', 'blue', 'green']]
            ax.legend(handles, color_labels, title='Значения', loc='upper right')

            # Настраиваем внешний вид
            plt.tight_layout()
            plt.show()

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные для построения графика")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при построении графика: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FeedRequirementCalculator(root)
    root.mainloop()