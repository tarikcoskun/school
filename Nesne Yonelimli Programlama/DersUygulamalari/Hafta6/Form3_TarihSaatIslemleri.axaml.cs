using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta6;

// DateTime özelliklerini (Now, Today, Year, Month, AddDays...) listBox1'e yazar. tarih ve saat seçicileri bugünle açılır.
public partial class Form3_TarihSaatIslemleri : Window
{
    public Form3_TarihSaatIslemleri()
    {
        InitializeComponent();

        dateTimePicker1.SelectedDate = DateTime.Today;
        dateTimePicker2.SelectedDate = DateTime.Today;
        dateTimePicker3.SelectedTime = DateTime.Now.TimeOfDay;
    }

    // Opened, pencere ilk kez çizilmeden önce çalışır. Loaded ise ilk çizimden sonra gelir,
    // bu yüzden liste bir anlığına boş görünürdü.
    private void Form3_TarihSaatIslemleri_Opened(object? sender, EventArgs e)
    {
        listBox1.Items.Add(DateTime.Now.ToString());
        listBox1.Items.Add(DateTime.Today.ToString());
        listBox1.Items.Add(DateTime.Today.Year.ToString());
        listBox1.Items.Add(DateTime.Today.Month.ToString());
        listBox1.Items.Add(DateTime.Today.Day.ToString());
        listBox1.Items.Add(DateTime.Today.Hour.ToString());
        listBox1.Items.Add(DateTime.Now.Hour.ToString());
        listBox1.Items.Add(DateTime.Today.AddDays(12).ToString());
        DateTime dt = new DateTime();
        DateTime dt1 = new DateTime(1998, 2, 8);
        label1.Text = dateTimePicker1.SelectedDate.Value.AddDays(12).ToString();
        label1.Text = dateTimePicker1.SelectedDate.Value.DayOfWeek.ToString();
    }

}
