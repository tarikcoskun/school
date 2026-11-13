using System;
using System.Collections.Generic;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta3;

// listBox1'deki sayıları tek-çift olarak ayırır. tekler küçükten büyüğe, çiftler büyükten küçüğe.
public partial class Form2_TekCiftAyirma : Window
{
    public Form2_TekCiftAyirma()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        listBox1.Items.Clear();

        Random rastgele = new Random();

        for (int i = 0; i < 20; i++)
        {
            listBox1.Items.Add(rastgele.Next(1, 500));
        }
    }

    private void Button2_Click(object sender, RoutedEventArgs e)
    {
        List<int> tek_sayilar = new List<int>();
        List<int> cift_sayilar = new List<int>();

        for (int i = 0; i < listBox1.Items.Count; i++)
        {
            int sayi_degeri = Convert.ToInt32(listBox1.Items[i]);

            if (sayi_degeri % 2 == 0)
                cift_sayilar.Add(sayi_degeri);
            else
                tek_sayilar.Add(sayi_degeri);
        }

        tek_sayilar.Sort();
        cift_sayilar.Sort();
        cift_sayilar.Reverse();
        listBox2.ItemsSource = tek_sayilar;
        listBox3.ItemsSource = cift_sayilar;
    }
}
