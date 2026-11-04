using System;
using System.Linq;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;

namespace DersUygulamalari.Hafta6;

public partial class Form4 : Window
{
    public Form4()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        TimeSpan tarih_fark = DateTime.Today - dateTimePicker1.SelectedDate.Value;
        int fark = tarih_fark.Days;
        int yillar = fark / 365;
        int gunler = fark % 365;
        textBox1.Text = yillar.ToString() + " yıl " + gunler.ToString() + " gündür yaşıyorsun";
    }
}
