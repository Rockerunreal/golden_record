using System;
using System.IO;
using System;
using System.IO;
using System.ComponentModel.DataAnnotations;


public class Mainji
{

    public static void Main()
    {
        var wholeStart = DateTime.Now; 
        List<List<string>> csvData = ReadCsvToList("\\data.csv"); //C:\Users\1airf\Downloads\Telegram Desktop\Golden_dataзкудфые\Golden_data\uploads \"C:\\\\Users\\\\1airf\\\\Desktop\\\\y.txt
        Dictionary<string, List<string>> result = GetGoldenDict(data: Thing(data: csvData, identificatorMask: [22, 21, 2], accuracyMask: [1, 1, 1], globalAccuracy: 2), idIndex: 0, updDateIndex: 45);
        string logpath = "\\RESULT.TXT";
        List<string> toWrite = new List<string>();
        foreach (string key in result.Keys)
        {
            string temp = "";
            toWrite.Add($"key: {key}\nValues:\n");
            foreach (string value in result[key])
            {
                temp += value + "; ";
            }
            toWrite.Add(temp+"\n");
        }
        File.WriteAllLines(logpath, toWrite);
        Console.WriteLine($"We done! it took: {(DateTime.Now - wholeStart)/60} mins"); 
    }


    public static List<List<string>> ReadCsvToList(string filePath)
    {
        if (!File.Exists(filePath))
            throw new FileNotFoundException("CSV file not found.", filePath);

        string[] lines = File.ReadAllLines(filePath);

        List<List<string>> result = new List<List<string>>(0);

        foreach (string line in lines)
        {
            result.Add(line.Split(',').ToList());
        }

        return result;
    }




    public static bool DamerauLevenshteinDistanceSlow(string s1, string s2, int etalon)
    {
        // Переворачиваем строки не забыть убрать после прихода 
        if ((s1 == "" )||( s2 == ""))
        {
            return false;
        }

        int lenS1 = s1.Length, lenS2 = s2.Length;


        int[] prevRow = new int[lenS2 + 1];
        int[] currRow = new int[lenS2 + 1];
        int[] prevPrevRow = new int[lenS2 + 1];

        for (int i = 0; i <= lenS2; i++)
            prevRow[i] = i;

        for (int i = 1; i <= lenS1; i++)
        {
            currRow[0] = i;

            for (int j = 1; j <= lenS2; j++)
            {
                int cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;

                currRow[j] = Math.Min(
                    Math.Min(prevRow[j] + 1, currRow[j - 1] + 1), 
                    prevRow[j - 1] + cost 
                );

           
                if (i > 1 && j > 1 && s1[i - 1] == s2[j - 2] && s1[i - 2] == s2[j - 1])
                {
                    currRow[j] = Math.Min(currRow[j], prevPrevRow[j - 2] + cost);
                }
            }


            if (currRow.Min() > etalon)
            {
                return false;
            }

            
            Array.Copy(prevRow, prevPrevRow, lenS2 + 1);
            Array.Copy(currRow, prevRow, lenS2 + 1);
            Array.Clear(currRow, 0, lenS2 + 1);
        }

        
        return prevRow[lenS2] <= etalon;
    }

    public static Dictionary<string, List<List<string>>> Thing(
        List<List<string>> data,
        List<int> identificatorMask,
        List<int> accuracyMask,
        int globalAccuracy = 1)
    {
        var sorttime = DateTime.Now;
        SortByColumnDescending(data, identificatorMask[0]);
        Console.Write($"time to sort: {DateTime.Now - sorttime}");
        int goldGuys = 0;
        int totalPop = 0;
        int totalIterations = data.Count;
        int linearPointer = 1;
        int quadraticPointer;
        int idPointer;
        int idPointerLimit = identificatorMask.Count;
        var toPop = new HashSet<int> { };
        var result = new Dictionary<string, List<List<string>>>();
        double medianTime = 0;

        while (linearPointer < data.Count)
        {
            //Console.WriteLine();
            toPop = new HashSet<int> { };
            var subResult = new List<List<string>>();
            quadraticPointer = linearPointer + 1;
            //var start = DateTime.Now;
            int iterationsLeft = data.Count;

            Console.WriteLine($"{iterationsLeft} {totalIterations - iterationsLeft}");
            bool gotUnsortedOnFirst = false;
            while ((quadraticPointer < iterationsLeft)&&(!gotUnsortedOnFirst))
            {
                
                int currentAccuracy = 0;
                idPointer = 0;
                while ((idPointer < idPointerLimit) && (((data[linearPointer].Count >= 47) && (data[quadraticPointer].Count >= 47))))
                {


                    
                    List<string> yx = data[quadraticPointer];
                    string x = data[linearPointer][identificatorMask[idPointer]];
                    string y = data[quadraticPointer][identificatorMask[idPointer]];
                    if (DamerauLevenshteinDistanceSlow(x, y, accuracyMask[idPointer]))
                    {
                        //Console.WriteLine($"{x} {x.Count()} {y.Count()} {(x, y, accuracyMask[idPointer])}");
                        currentAccuracy++;
                    }
                    else
                    {
                        if (idPointer == 0)
                        {
                            gotUnsortedOnFirst = true;
                        }
                    }

                    idPointer++;

                    if (currentAccuracy >= globalAccuracy)
                    {
                        toPop.Add(quadraticPointer - 1);
                        break;
                    }
                }
                quadraticPointer++;
            }
            //var poptime = DateTime.Now;
            subResult.Add(data[0]);
            data.RemoveAt(0);
            totalPop++;
            int counter = 0;

            foreach (int i in toPop)
            {
                subResult.Add(data[i-counter]);
                data.RemoveAt(i-counter);
                totalPop++;
                counter++;
                //Console.WriteLine(counter);
            }
            //Console.WriteLine($"time to pop: {DateTime.Now - poptime}");

            result[goldGuys.ToString()] = subResult;
            //double end = (DateTime.Now - start).TotalSeconds;
            //medianTime += end;
            //Console.WriteLine($"Time consumed for this iteration: {end}\nMedian time: {medianTime / (goldGuys + 1)}");

            goldGuys++;
            //double medianPop = (double)totalPop / goldGuys;
            //Console.WriteLine($"Gold guys found: {goldGuys}");
            //Console.WriteLine($"Median pop: {medianPop}");
            //Console.WriteLine($"Approx time ~ {(((totalIterations / medianPop) * (medianTime / (goldGuys + 1))) / (3600*medianPop))} hours\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
        }

        return result;
    }


    static void SortByColumnDescending(List<List<string>> data, int index)
    {
        data.Sort((row1, row2) =>
        {
            if (!(index >= row1.Count || index >= row2.Count)){


                return CompareByAsciiDescending(row1[index], row2[index]);
            }
            else
            {
                return 0;
            }
        });
    }

    static int CompareByAsciiDescending(string str1, string str2)
    {
        int len = Math.Min(str1.Length, str2.Length);
        for (int i = 0; i < len; i++)
        {
            int diff = str2[i] - str1[i]; 
            if (diff != 0) return diff;
        }
        return str2.Length - str1.Length;
    }

    public static Dictionary<string, List<string>> GetGoldenDict(
        Dictionary<string, List<List<string>>> data,
        int idIndex = 0,
        int updDateIndex = -2)
    {
        var mergedData = new Dictionary<string, List<string>>();
        bool dataPreference = false;
        int mergePointer = 1;
        int mergePointerLimit = data["0"][0].Count - 1;
        int variantPointer;
        int variantPointerLimit;

        foreach (var key in data.Keys)
        {
            mergedData[key] = new List<string>(data[key][^1]);
            variantPointerLimit = data[key].Count;
            variantPointer = 0;

            while (variantPointer < variantPointerLimit)
            {
                while (mergePointer < mergePointerLimit)
                {
                    if (string.IsNullOrEmpty(data[key][variantPointer][mergePointer]))
                    {
                        mergePointer++;
                    }
                    else if (string.IsNullOrEmpty(mergedData[key][mergePointer]))
                    {
                        mergedData[key][mergePointer] = data[key][variantPointer][mergePointer];
                        mergePointer++;
                    }
                    else
                    {
                        string[] updDateStaticParts = mergedData[key][updDateIndex].Split(':');
                        string[] updDatePointerParts = data[key][variantPointer][updDateIndex].Split(':');

                        DateTime updDateStatic, updDatePointer;

                        try
                        {
                            updDateStatic = new DateTime(
                                int.Parse(updDateStaticParts[0]),
                                int.Parse(updDateStaticParts[1]),
                                int.Parse(updDateStaticParts[2]),
                                int.Parse(updDateStaticParts[3]),
                                int.Parse(updDateStaticParts[4]),
                                int.Parse(updDateStaticParts[5])
                            );

                            updDatePointer = new DateTime(
                                int.Parse(updDatePointerParts[0]),
                                int.Parse(updDatePointerParts[1]),
                                int.Parse(updDatePointerParts[2]),
                                int.Parse(updDatePointerParts[3]),
                                int.Parse(updDatePointerParts[4]),
                                int.Parse(updDatePointerParts[5])
                            );
                        }
                        catch (FormatException)
                        {
                            updDateStatic = new DateTime(1999, 1, 2, 2, 2, 2);
                            updDatePointer = new DateTime(1999, 2, 2, 2, 2, 2);
                        }

                        if (updDateStatic > updDatePointer)
                        {
                            mergePointer++;
                        }
                        else
                        {
                            mergedData[key][mergePointer] = data[key][variantPointer][mergePointer];
                            mergePointer++;
                        }
                    }
                }
                variantPointer++;
            }
        }

        return mergedData;
    }
}