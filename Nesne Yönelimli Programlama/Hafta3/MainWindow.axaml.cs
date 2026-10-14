using System;
using System.Collections.Generic;
using System.Linq;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace Hafta3;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        int[] sayilar = new int[20];

        Random rastgele = new Random();

        int sayi1 = Convert.ToInt32(textBox1.Text);
        int sayi2 = Convert.ToInt32(textBox2.Text);

        for (int i = 0; i < 20; i++)
        {
            listBox1.Items.Add(rastgele.Next(1, 500));
        }
    }

    private void Button2_Click(object sender, RoutedEventArgs e)
    {
        /*
        List<int> tek_sayilar = new List<int>();
        List<int> cift_sayilar = new List<int>();

        int sayi_degeri = 0;

        for (int i = 0; i < listBox1.Items.Count; i++)
        {
            sayi_degeri = Convert.ToInt32(listBox1.Items[i]);

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
        */

        /*
        string sehir = "";
        int en_uzun_sehir_idx = 0;
        int en_buyuk_sehir_uzunluk = 0;

        for (int i = 0; i < listBox2.Items.Count; i++)
        {
            sehir = listBox2.Items[i].ToString();

            if (sehir?.Length > en_buyuk_sehir_uzunluk)
            {
                en_buyuk_sehir_uzunluk = sehir.Length;
                en_uzun_sehir_idx = i;
            }
        }

        listBox3.Items.Add(listBox2.Items[en_uzun_sehir_idx]);
        */

        /*
        for (int i = 0; i < listBox1.Items.Count; i++)
        {
            int sayi = Convert.ToInt32(listBox1.Items[i]);

            if (sayi % 2 == 0)
            {
                listBox2.Items.Add(sayi);
            }
            else
            {
                listBox3.Items.Add(sayi);
            }
        }

        var cift = listBox2.Items.Cast<int>().OrderBy(x => x).ToList();
        listBox2.Items.Clear();

        foreach (int n in cift)
        {
            listBox2.Items.Add(n);
        }

        var tek = listBox3.Items.Cast<int>().OrderBy(x => x).ToList();
        listBox3.Items.Clear();

        foreach (int n in tek)
        {
            listBox3.Items.Add(n);
        }
        */
    }

    List<string> secimler = new List<string>();

    private void ListBox2_SelectionChanged(object? sender, SelectionChangedEventArgs e)
    {
        foreach (ListBoxItem item in e.AddedItems)
        {
            secimler.Add(item.Content?.ToString() ?? "");
        }

        foreach (ListBoxItem item in e.RemovedItems)
        {
            secimler.Remove(item.Content?.ToString() ?? "");
        }
    }

    private void Button3_Click(object? sender, RoutedEventArgs e)
    {
        listBox3.Items.Clear();

        foreach (string item in secimler)
        {
            listBox3.Items.Add(item);
        }
    }
}
