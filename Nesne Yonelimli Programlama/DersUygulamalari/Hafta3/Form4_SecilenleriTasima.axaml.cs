using System;
using System.Collections.Generic;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta3;

// listBox1'de seçilen şehirleri ">>" butonuyla listBox2'ye aktarır.
public partial class Form4_SecilenleriTasima : Window
{
    public Form4_SecilenleriTasima()
    {
        InitializeComponent();
    }

    // Opened, pencere ilk kez çizilmeden önce çalışır. Loaded ise ilk çizimden sonra gelir,
    // bu yüzden liste bir anlığına boş görünürdü.
    private void Form4_SecilenleriTasima_Opened(object? sender, EventArgs e)
    {
        listBox1.Items.Clear();
        listBox1.Items.Add("rize");
        listBox1.Items.Add("bitlis");
        listBox1.Items.Add("yozgat");
        listBox1.Items.Add("istanbul");
        listBox1.Items.Add("ankara");
    }

    List<string> secimler = new List<string>();

    private void ListBox1_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        foreach (object item in e.AddedItems)
        {
            secimler.Add(item.ToString() ?? "");
        }

        foreach (object item in e.RemovedItems)
        {
            secimler.Remove(item.ToString() ?? "");
        }
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        listBox2.Items.Clear();

        foreach (string item in secimler)
        {
            listBox2.Items.Add(item);
        }
    }
}
