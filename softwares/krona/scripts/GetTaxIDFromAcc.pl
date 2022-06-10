#!/usr/bin/env perl

# Copyright © 2011, Battelle National Biodefense Institute (BNBI);
# all rights reserved. Authored by: Brian Ondov, Nicholas Bergman, and
# Adam Phillippy
#
# See the LICENSE.txt file included with this software for license information.


use strict;

BEGIN
{
	use File::Basename;
	use Cwd 'abs_path';
	use lib dirname(abs_path($0)) . "/../lib";
	use KronaTools;
}

use Getopt::Long;

my $help;
my $prepend;
my $append;
my $tax;

GetOptions
(
	'h' => \$help,
	'help' => \$help,
	'p' => \$prepend,
	'a' => \$append,
	'tax=s' => \$tax
);

if ( defined $tax )
{
	setOption('taxonomy', $tax);
}

if ( $help )
{
	print '
Description:

   Translates accessions (from arguments or <stdin>) to NCBI taxonomy IDs. The
   accession can be bare or in the fourth field of pipe notation (e.g.
   "gi|12345|xx|ABC123.1|", ignoring fasta tag markers [">"]). Inputs that are
   bare numbers will be assumed to be taxonomy IDs already and preserved.
   Accessions with no taxonomy IDs in the database will return 0.

Usage:

   ktGetTaxIDFromAcc [options] [acc1 acc2 ...] [< acc_list] > tax_ID_list

   Command line example:
   
      ktGetTaxIDFromAcc A00001.1 A00002.1

   Fasta tag example:

      grep ">" sequence

Options:

   -p  Prepend tax IDs to the original lines (separated by tabs).
  
   -a  Append tax IDs to the original lines (separated by tabs).

';
	exit;
}

if ( $prepend && $append )
{
	ktWarn('Both -p and -a specified. Only -a will be used.');
	$prepend = 0;
}

my $stdin;

if ( @ARGV == 0 )
{
	$stdin = 1;
}

while ( my $in = $stdin ? <STDIN> : shift @ARGV )
{
	chomp $in;
	
	if ( $in eq "" )
	{
		print "\n";
		next;
	}
	
	if ( $append )
	{
		print "$in\t";
	}
	
	print getTaxIDFromAcc(getAccFromSeqID($in));
	
	if ( $prepend )
	{
		print "\t$in";
	}
	
	print "\n";
}

printWarnings();
