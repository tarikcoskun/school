using Avalonia.Controls;
using Avalonia.Interactivity;

namespace DersUygulamalari.Hafta4;

// textBox1'deki cümleye string metotlarını (Substring, Trim, IndexOf, ToUpper, Remove, Replace, Insert...) uygular, sonuçları numaralı olarak listBox1'e yazar.
public partial class Form1_StringMetotlari : Window
{
    public Form1_StringMetotlari()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        string cumle = textBox1.Text ?? "";

        listBox1.Items.Add("1 - " + cumle.Substring(4));
        listBox1.Items.Add("2 - " + cumle.Substring(8, 12));
        listBox1.Items.Add("3 - " + cumle.Trim());
        listBox1.Items.Add("4 - " + cumle.TrimStart());
        listBox1.Items.Add("5 - " + cumle.IndexOf("Ü"));
        listBox1.Items.Add("6 - " + cumle.IndexOf("Üniversitesi"));
        listBox1.Items.Add("7 - " + cumle.ToLower());
        listBox1.Items.Add("8 - " + cumle.ToUpper());
        listBox1.Items.Add("9 - " + cumle.Remove(5));
        listBox1.Items.Add("10 - " + cumle.Remove(5, 4));
        listBox1.Items.Add("11 - " + cumle.Replace("a", "z"));
        listBox1.Items.Add("12 - " + cumle.Insert(10, "fatih"));
        listBox1.Items.Add("13 - " + cumle.Length);
    }
}
