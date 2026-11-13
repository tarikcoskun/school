using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta6;

// dateTimePicker1'de seçilen doğum tarihinden bugüne kaç yıl ve gün geçtiğini label1'e yazar.
public partial class Form4_YasHesaplama : Window
{
    public Form4_YasHesaplama()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        TimeSpan tarih_fark = DateTime.Today - dateTimePicker1.SelectedDate.Value;
        int fark = tarih_fark.Days;
        int yillar = fark / 365;
        int gunler = fark % 365;
        label1.Text = yillar.ToString() + " yıl " + gunler.ToString() + " gündür yaşıyorsun";
    }
}
