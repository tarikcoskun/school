using System;
using System.Linq;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;

namespace DersUygulamalari.Hafta6;

public partial class Form1 : Window
{
    public Form1()
    {
        InitializeComponent();
    }

    private void Button1_Click(object sender, RoutedEventArgs e)
    {
        textBox1.Text = richTextBox1.Lines.Count().ToString();
        richTextBox1.SelectionBackColor = Colors.Red;
        richTextBox1.SelectionColor = Colors.Yellow;

        richTextBox1.AppendText("\n" + textBox1.Text);
        richTextBox1.Font = new Font("Consolas", 18f, FontWeight.Bold);
        textBox1.Text = richTextBox1.Find("fatih").ToString();
        textBox1.Text = richTextBox1.Size.Height.ToString();
        textBox1.Text = richTextBox1.Text;
        textBox1.Text = richTextBox1.SelectionLength.ToString();
        textBox1.Text = richTextBox1.SelectedText.Count().ToString();
        textBox1.Text = richTextBox1.SelectedText.Insert(3, "fatih");
        textBox1.Text = richTextBox1.SelectedText.IndexOf('a').ToString();
        textBox1.Text = richTextBox1.SelectedText.Replace('a', 'e');
        // textBox1.Text = richTextBox1.SelectedText.Remove(4);
        // textBox1.Text = richTextBox1.SelectedText.Remove(4, 3);

        richTextBox1.Select(0, richTextBox1.Lines[0].Length);
        richTextBox1.SelectionBackColor = Colors.Red;
    }
}
