using System;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta4;

public partial class Form1 : Window
{
    public Form1()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        string cumle = "Marmara Üniversitesi Yapay Zeka Operatörlüğü   ";
        textBox1.Text = cumle;
        listBox1.Items.Add(cumle.Substring(4));
        listBox1.Items.Add(cumle.Substring(8, 12));
        listBox1.Items.Add(cumle.Trim());
        listBox1.Items.Add(cumle.TrimStart());
        listBox1.Items.Add(cumle.IndexOf("Ü"));
        listBox1.Items.Add(cumle.IndexOf("Üniversitesi"));
        listBox1.Items.Add(cumle.ToLower());
        listBox1.Items.Add(cumle.ToUpper());
        listBox1.Items.Add(cumle.Remove(5));
        listBox1.Items.Add(cumle.Remove(5, 4));
        listBox1.Items.Add(cumle.Replace("a", "z"));
        listBox1.Items.Add(cumle.Insert(10, "fatih"));
        listBox1.Items.Add(cumle.Length);
    }
}
