using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta4;

// textBox1'deki kelimeleri kısadan uzuna sıralar, listBox1'e yazar.
public partial class Form3_KelimeleriUzunlugaGoreSiralama : Window
{
    public Form3_KelimeleriUzunlugaGoreSiralama()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        string[] kelimeler = textBox1.Text!.Split(" ");
        Array.Sort(kelimeler, (a, b) => a.Length - b.Length);

        foreach (string kelime in kelimeler)
        {
            listBox1.Items.Add(kelime);
        }
    }
}
