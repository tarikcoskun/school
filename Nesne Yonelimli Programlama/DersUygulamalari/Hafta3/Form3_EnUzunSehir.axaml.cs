using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta3;

// listBox1'deki şehirlerden adı en uzun olanı bulur.
public partial class Form3_EnUzunSehir : Window
{
    public Form3_EnUzunSehir()
    {
        InitializeComponent();
    }

    // Opened, pencere ilk kez çizilmeden önce çalışır. Loaded ise ilk çizimden sonra gelir,
    // bu yüzden liste bir anlığına boş görünürdü.
    private void Form3_EnUzunSehir_Opened(object? sender, EventArgs e)
    {
        listBox1.Items.Clear();
        listBox1.Items.Add("rize");
        listBox1.Items.Add("bitlis");
        listBox1.Items.Add("yozgat");
        listBox1.Items.Add("istanbul");
        listBox1.Items.Add("ankara");
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        string? sehir = "";
        int en_uzun_sehir_idx = 0;
        int en_buyuk_sehir_uzunluk = 0;

        for (int i = 0; i < listBox1.Items.Count; i++)
        {
            sehir = listBox1.Items[i]?.ToString();

            if (sehir?.Length > en_buyuk_sehir_uzunluk)
            {
                en_buyuk_sehir_uzunluk = sehir.Length;
                en_uzun_sehir_idx = i;
            }
        }

        listBox2.Items.Add(listBox1.Items[en_uzun_sehir_idx]);
    }
}
