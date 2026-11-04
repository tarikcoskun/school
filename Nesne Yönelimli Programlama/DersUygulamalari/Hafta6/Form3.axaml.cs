using System;
using System.Linq;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;

namespace DersUygulamalari.Hafta6;

public partial class Form3 : Window
{
    public Form3()
    {
        InitializeComponent();

        dateTimePicker1.SelectedDate = DateTime.Today;
        dateTimePicker2.SelectedDate = DateTime.Today;
        dateTimePicker3.SelectedTime = DateTime.Now.TimeOfDay;
    }

    private void Form3_Load(object sender, RoutedEventArgs e)
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
        textBox1.Text = dateTimePicker1.SelectedDate.Value.AddDays(12).ToString();
        textBox1.Text = dateTimePicker1.SelectedDate.Value.DayOfWeek.ToString();
    }

}
