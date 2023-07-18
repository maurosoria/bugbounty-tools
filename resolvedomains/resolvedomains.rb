#!/usr/bin/env ruby
# DNS Resolver - A script to resolve domain names to IP addresses.
# Usage: ruby dns_resolver.rb [options] < input_file
#        or
#        cat input_file | ruby dns_resolver.rb [options]
# Options:
#   -v, --verbose    Display verbose output with hostname and IP address.

require 'resolv'
require 'set'
require 'optparse'

class Resolver
  attr_reader :ip_addresses

  def initialize(string)
    @ip_addresses = []
    if Resolver.is_ip_addr?(string)
      @ip_addresses << string
    else
      resolved = Resolver.resolve(string)
      @ip_addresses += resolved unless resolved.nil?
    end
  end

  def is_domain_here?(domain)
    ip_addresses = Resolver.resolve(domain)
    return false if ip_addresses.nil?
    ip_addresses.any? { |ip_addr| @ip_addresses.include?(ip_addr) }
  end

  def self.is_ip_addr?(string)
    !!(string =~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/)
  end

  def self.resolve(domain)
    begin
      Resolv.getaddresses(domain).map(&:to_s)
    rescue Resolv::ResolvError, Resolv::NoAnswer, Resolv::NoNameservers => e
      nil
    end
  end
end

def solve_ip_addresses(s, verbose)
  r = Resolver.new(s)
  if verbose
    r.ip_addresses.map { |ip| "#{s} #{ip}" }
  else
    r.ip_addresses
  end
end

def main(options)
  lines = $stdin.read.split("\n").uniq
  resolved = Set.new
  lines.each_slice(30) do |batch|
    batch_resolved = batch.map { |line| solve_ip_addresses(line, options[:verbose]) }.flatten.uniq
    batch_resolved.each do |ip_addr|
      unless resolved.include?(ip_addr)
        resolved << ip_addr
        puts ip_addr
      end
    end
  end
end

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: ruby dns_resolver.rb [options] < input_file\n       or\n       cat input_file | ruby dns_resolver.rb [options]"
  opts.on('-v', '--verbose', 'Display verbose output with hostname and IP address.') do
    options[:verbose] = true
  end
  opts.on('-h', '--help', 'Display this help message.') do
    puts opts
    exit
  end
end.parse!

main(options)